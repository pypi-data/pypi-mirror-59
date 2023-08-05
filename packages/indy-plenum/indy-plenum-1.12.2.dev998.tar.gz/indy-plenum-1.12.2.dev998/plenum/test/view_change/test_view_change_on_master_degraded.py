import types

import pytest

from plenum.common.throughput_measurements import RevivalSpikeResistantEMAThroughputMeasurement
from plenum.server.view_change.view_changer import ViewChanger
from plenum.test.delayers import delayNonPrimaries
from plenum.test.helper import waitForViewChange, \
    sdk_send_random_and_check
from plenum.test.node_catchup.helper import ensure_all_nodes_have_same_data, waitNodeDataEquality
from plenum.test.test_node import get_master_primary_node, getPrimaryReplica, \
    ensureElectionsDone
from plenum.test.view_change.helper import simulate_slow_master, node_sent_instance_changes_count

nodeCount = 7


@pytest.fixture(scope="module")
def tconf(tconf):
    old_throughput_measurement_class = tconf.throughput_measurement_class
    old_throughput_measurement_params = tconf.throughput_measurement_params
    old_timeout = tconf.ACC_MONITOR_TIMEOUT
    old_delta = tconf.ACC_MONITOR_TXN_DELTA_K
    old_check_time = tconf.PerfCheckFreq

    tconf.throughput_measurement_class = RevivalSpikeResistantEMAThroughputMeasurement
    tconf.throughput_measurement_params = {
        'window_size': 2,
        'min_cnt': 3
    }
    tconf.ACC_MONITOR_TIMEOUT = 3
    tconf.ACC_MONITOR_TXN_DELTA_K = 0
    tconf.PerfCheckFreq = 5

    yield tconf

    tconf.throughput_measurement_class = old_throughput_measurement_class
    tconf.throughput_measurement_params = old_throughput_measurement_params
    tconf.ACC_MONITOR_TIMEOUT = old_timeout
    tconf.ACC_MONITOR_TXN_DELTA_K = old_delta
    tconf.PerfCheckFreq = old_check_time


# noinspection PyIncorrectDocstring


def test_view_change_on_performance_degraded(looper, txnPoolNodeSet, viewNo,
                                             sdk_pool_handle,
                                             sdk_wallet_steward):
    """
    Test that a view change is done when the performance of master goes down
    Send multiple requests from the client and delay some requests by master
    instance so that there is a view change. All nodes will agree that master
    performance degraded
    """
    old_primary_node = get_master_primary_node(list(txnPoolNodeSet))

    for n in txnPoolNodeSet:
        n.view_changer.on_master_degradation()

    waitForViewChange(looper, txnPoolNodeSet, expectedViewNo=viewNo + 1)

    ensureElectionsDone(looper=looper, nodes=txnPoolNodeSet)
    ensure_all_nodes_have_same_data(looper, nodes=txnPoolNodeSet)
    new_primary_node = get_master_primary_node(list(txnPoolNodeSet))
    assert old_primary_node.name != new_primary_node.name
    waitNodeDataEquality(looper, *txnPoolNodeSet)


def test_view_change_on_quorum_of_master_degraded(txnPoolNodeSet, looper,
                                                  sdk_pool_handle,
                                                  sdk_wallet_steward,
                                                  viewNo):
    """
    Node will change view even though it does not find the master to be degraded
    when a quorum of nodes agree that master performance degraded
    """

    m_primary_node = get_master_primary_node(list(txnPoolNodeSet))

    # Delay processing of PRE-PREPARE from all non primary replicas of master
    # so master's performance falls and view changes
    delayNonPrimaries(txnPoolNodeSet, 0, 10)

    pr = getPrimaryReplica(txnPoolNodeSet, 0)
    relucatantNode = pr.node

    # Count sent instance changes of all nodes
    sentInstChanges = {}
    for n in txnPoolNodeSet:
        sentInstChanges[n.name] = node_sent_instance_changes_count(n)

    # Node reluctant to change view, never says master is degraded
    relucatantNode.monitor.isMasterDegraded = types.MethodType(
        lambda x: False, relucatantNode.monitor)

    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_steward, 4)

    for n in txnPoolNodeSet:
        n.checkPerformance()

    # Check that view change happened for all nodes
    waitForViewChange(looper, txnPoolNodeSet, expectedViewNo=viewNo + 1)

    # All nodes except the reluctant node should have sent a view change and
    # thus must have called `sendInstanceChange`
    for n in txnPoolNodeSet:
        if n.name != relucatantNode.name:
            assert node_sent_instance_changes_count(n) > sentInstChanges.get(n.name, 0)
        else:
            assert node_sent_instance_changes_count(n) == sentInstChanges.get(n.name, 0)

    ensureElectionsDone(looper=looper, nodes=txnPoolNodeSet)
    new_m_primary_node = get_master_primary_node(list(txnPoolNodeSet))
    assert m_primary_node.name != new_m_primary_node.name
    ensure_all_nodes_have_same_data(looper, nodes=txnPoolNodeSet)
