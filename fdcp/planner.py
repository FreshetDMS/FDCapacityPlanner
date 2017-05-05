from vsvbp.solver import optimize
from fdcp.aws import *
import logging
import sys
from sets import Set
from random import shuffle, randint, seed
from timeit import default_timer as timer
import itertools

logging.basicConfig(format='%(asctime)s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger('planner')

MILLION = 1000000
HUNDRED_THOUSAND = 100000
INDEX_SIZE = 10
FLUSH_DELAY_SECONDS = 30


class Topic(object):
    def __init__(self, name, produce_rate, mean_msg_size, num_partitions, replication_factor, num_consumers,
                 num_replays, mean_replay_rate, max_consumer_lag, retention_period,
                 allocate_read_capacity_for_replicas=False):
        self.name = name
        self.produce_rate = produce_rate
        self.mean_msg_size = mean_msg_size
        self.num_partitions = num_partitions
        self.replication_factor = replication_factor
        self.num_consumers = num_consumers
        self.num_replays = num_replays
        self.mean_replay_rate = mean_replay_rate
        self.max_consumer_lag = max_consumer_lag
        self.allocate_read_capacity_for_replicas = allocate_read_capacity_for_replicas
        self.retention_period = retention_period

    def partitions(self):
        result = []
        per_partition_produce_rate_mbps = ((self.produce_rate * self.mean_msg_size) / MILLION) / self.num_partitions
        size_req = per_partition_produce_rate_mbps * self.retention_period * 3600
        per_partition_replay_rate = ((self.mean_replay_rate * self.mean_msg_size) / MILLION) / self.num_partitions
        per_partition_mem_requirements = max(self.max_consumer_lag * per_partition_produce_rate_mbps,
                                             FLUSH_DELAY_SECONDS * per_partition_produce_rate_mbps) + \
                                        per_partition_replay_rate
        reads = self.num_replays * per_partition_replay_rate
        ebs_bw_requirement = per_partition_produce_rate_mbps + reads
        reads_pct = float(reads) / ebs_bw_requirement
        network_in_requirement = per_partition_produce_rate_mbps
        network_out_requirement = (self.num_consumers + self.replication_factor - 1) * \
                                  per_partition_produce_rate_mbps + self.num_replays * per_partition_replay_rate
        for p in range(self.num_partitions):
            result.append(Partition(per_partition_mem_requirements, network_in_requirement, network_out_requirement,
                                    ebs_bw_requirement, size_req, reads_pct, self.name, p, 0))
            for r in range(self.replication_factor - 1):
                result.append(
                    Partition(per_partition_mem_requirements, network_in_requirement, network_out_requirement,
                              ebs_bw_requirement if self.allocate_read_capacity_for_replicas else
                              per_partition_produce_rate_mbps,
                              size_req,
                              reads_pct if self.allocate_read_capacity_for_replicas else 0.0, self.name, p,
                              r + 1))
        return result


class LogStoreWorkload(object):
    def __init__(self):
        self.topics = []

    def add_topic(self, topic):
        self.topics.append(topic)

    def partitions(self):
        items = []
        for topic in self.topics:
            items.extend(topic.partitions())
        return items


class LogStoreCapacityPlanner(object):
    def __init__(self, node_types, workload):
        # This should be fixed to support instance types from different categories
        # We need to get retention period as a parameter to calculate storage costs
        self.node_types = sorted(node_types, key=lambda n: n.instance_type.vcpus())
        self.workload = workload

    def find_bin_lower_bound(self):
        partitions = self.workload.partitions()
        max_network_out = max(partitions, key=lambda p: p.network_out).network_out
        max_network_in = max(partitions, key=lambda p: p.network_in).network_in
        max_storage_bw = max(partitions, key=lambda p: p.storage_bw).storage_bw
        max_size = max(partitions, key=lambda p: p.size).size
        max_mem = max(partitions, key=lambda p: p.memory).memory
        print max_network_out, max_network_in, max_storage_bw, max_size, max_mem
        for i, n in enumerate(self.node_types):
            if n.instance_type.memory() > max_mem and n.instance_type.network_bandwidth() > max_network_in and \
                            n.instance_type.network_bandwidth() > max_network_out and \
                            n.instance_type.storage_bandwidth() > max_storage_bw and \
                    n.instance_type.max_storage_size() > max_size:
                return i

    def plan(self):
        plans = []
        best_cost = sys.maxint
        best_config = None
        lb = self.find_bin_lower_bound()
        best_instance = self.node_types[lb]
        for i in range(lb, len(self.node_types)):
            node = self.node_types[i]
            logger.info("Running optimize with bin type: " + str(node))
            items = self.workload.partitions()
            shuffle(items)
            assignment = optimize(items, node, use_dp=False, aws=True)
            cost = sum([b.hourly_cost() if sum(b.utilization()) > 0 else 0 for b in assignment.bins])
            plans.append((assignment, node, cost))
            logger.info("Optimal bins: " + str(len(assignment.bins)) + " and cost: " + str(cost))
            if cost < best_cost:
                best_cost = cost
                best_instance = node
                best_config = assignment
        LogStoreCapacityPlanner.verify(best_config)
        return {'assignment': best_config, 'bin-type': best_instance, 'other-plans': plans}

    @classmethod
    def verify(cls, assignment):
        for b in assignment.bins:
            partitions = Set()
            for i in b.items:
                if partitions.intersection(Set([i.pid])):  # make this work across any capacity planner
                    raise RuntimeError('Replicas of same partition cannot be in same bin.')
                else:
                    partitions.add(i.pid)


# TODO: Need to understand Kafka network utilization

def bench():
    retention_period = 36
    consumer_lag = 40
    per_partition_arrival_rate = 1000000
    consumer_count = 3
    min_replay_count = 2
    replication_factor = 2
    message_size = 200
    log_count = [3200, 6400]
    partition_count = [400, 800]

    seed(12)

    for p, l in itertools.izip(partition_count, log_count):
        workload = LogStoreWorkload()
        for k in range(0, l / p):
            arrival_rate = (per_partition_arrival_rate / message_size) * p
            replay_rate = arrival_rate * 3
            workload.add_topic(Topic("topic-{}".format(k), arrival_rate, message_size, p, replication_factor,
                                     consumer_count, min_replay_count, replay_rate,
                                     consumer_lag, retention_period))

        cp = LogStoreCapacityPlanner([InstanceBin(InstanceType.D2_2X, StorageType.D2HDD)], workload)
        p = cp.plan()

        iterations = 1
        elpased_time = 0

        for i in range(0, iterations):
            start = timer()
            cp = LogStoreCapacityPlanner([InstanceBin(InstanceType.D2_2X, StorageType.D2HDD)], workload)
            p = cp.plan()
            elpased_time += timer() - start

        print 'mean execution time:', elpased_time / float(iterations)
        print 'items:', len(p['assignment'].items)
        print 'bins:', len(p['assignment'].bins)
        print '----------------------------------\n'
