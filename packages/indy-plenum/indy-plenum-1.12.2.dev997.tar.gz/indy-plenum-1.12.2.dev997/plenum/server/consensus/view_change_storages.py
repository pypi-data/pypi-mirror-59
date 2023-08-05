from _sha256 import sha256
from collections import defaultdict
from typing import Optional, List, Tuple

from common.serializers.json_serializer import JsonSerializer
from plenum.common.messages.node_messages import ViewChange, ViewChangeAck
from plenum.server.consensus.utils import replica_name_to_node_name


def view_change_digest(msg: ViewChange) -> str:
    msg_as_dict = msg._asdict()
#    msg_as_dict['checkpoints'] = [cp.__dict__ for cp in msg_as_dict['checkpoints']]
    serialized = JsonSerializer().dumps(msg_as_dict)
    return sha256(serialized).hexdigest()


class ViewChangeVotesForNode:
    """
    Storage for view change vote from some node for some view + corresponding acks
    """

    def __init__(self, quorums):
        self._view_change = None
        self._digest = None
        self._quorums = quorums
        self._acks = defaultdict(set)  # Dict[str, Set[str]]

    @property
    def digest(self) -> Optional[str]:
        """
        Returns digest of received view change message
        """
        return self._digest

    @property
    def view_change(self) -> Optional[ViewChange]:
        """
        Returns received view change
        """
        return self._view_change

    @property
    def is_confirmed(self) -> bool:
        """
        Returns True if received view change message and enough corresponding acks
        """
        if self._digest is None:
            return False

        return self._quorums.view_change_ack.is_reached(len(self._acks[self._digest]))

    def add_view_change(self, msg: ViewChange) -> bool:
        """
        Adds view change vote and returns boolean indicating if it found node suspicios
        """
        if self._view_change is None:
            self._view_change = msg
            self._digest = view_change_digest(msg)
            return self._validate_acks()

        return self._digest == view_change_digest(msg)

    def add_view_change_ack(self, msg: ViewChangeAck, frm: str) -> bool:
        """
        Adds view change ack and returns boolean indicating if it found node suspicios
        """
        self._acks[msg.digest].add(frm)
        return self._validate_acks()

    def update_quorums(self, quorums):
        self._quorums = quorums

    def _validate_acks(self) -> bool:
        digests = [digest for digest, acks in self._acks.items()
                   if self._quorums.weak.is_reached(len(acks))]

        if len(digests) > 1:
            return False

        if len(digests) < 1 or self._digest is None:
            return True

        return self._digest == digests[0]


class ViewChangeVotesForView:
    """
    Storage for view change votes for some view + corresponding acks
    """

    def __init__(self, quorums):
        self._votes = {}
        self._quorums = quorums

    @property
    def confirmed_votes(self) -> List[Tuple[str, str]]:
        return [[frm, node_votes.digest] for frm, node_votes in self._votes.items()
                if node_votes.is_confirmed]

    def get_view_change(self, frm: str, digest: str) -> Optional[ViewChange]:
        vc = self._get_vote(frm).view_change
        if vc is not None and view_change_digest(vc) == digest:
            return vc

    def add_view_change(self, msg: ViewChange, frm: str) -> bool:
        """
        Adds view change ack and returns boolean indicating if it found node suspicios
        """
        frm = replica_name_to_node_name(frm)
        return self._get_vote(frm).add_view_change(msg)

    def add_view_change_ack(self, msg: ViewChangeAck, frm: str) -> bool:
        """
        Adds view change ack and returns boolean indicating if it found node suspicios
        """
        frm = replica_name_to_node_name(frm)
        return self._get_vote(msg.name).add_view_change_ack(msg, frm)

    def clear(self):
        self._votes.clear()

    def update_quorums(self, quorums):
        for vote in self._votes.values():
            vote.update_quorums(quorums)

    def _get_vote(self, frm):
        if frm not in self._votes:
            self._votes[frm] = ViewChangeVotesForNode(self._quorums)
        return self._votes[frm]
