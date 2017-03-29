from operator import truediv, sub
from vsvbp.container import ConstrainedItem, Bin
from vsvbp.solver import optimize
import sys

MILLION = 1000000
HUNDRED_THOUSAND = 100000
INDEX_SIZE = 10
FLUSH_DELAY_SECONDS = 30


class EC2Instance(Bin):
    def __init__(self, type, vcpus, memory, network_bw, ebs_bw, cost):
        super(EC2Instance, self).__init__([memory, ebs_bw, network_bw, network_bw])
        self.memory = memory
        self.ebs_bw = ebs_bw
        self.network_bw = network_bw
        self.type = type
        self.vcpus = vcpus
        self.cost = cost

    def __repr__(self):
        return str([self.type, self.vcpus, self.capacities, self.remaining])

    def utilization(self):
        return map(truediv, map(sub, self.capacities, self.remaining), self.capacities)


class Topic(object):
    def __init__(self, name, produce_rate, mean_msg_size, num_partitions, replication_factor, num_consumers,
                 num_replays,
                 mean_replay_rate, max_consumer_lag):
        self.name = name
        self.produce_rate = produce_rate
        self.mean_msg_size = mean_msg_size
        self.num_partitions = num_partitions
        self.replication_factor = replication_factor
        self.num_consumers = num_consumers
        self.num_replays = num_replays
        self.mean_replay_rate = mean_replay_rate
        self.max_consumer_lag = max_consumer_lag

    def partitions(self):
        result = []
        per_partition_produce_rate_mbps = ((self.produce_rate * self.mean_msg_size) / MILLION) / self.num_partitions
        per_partition_replay_rate = ((self.mean_replay_rate * self.mean_msg_size) / MILLION) / self.num_partitions
        per_partition_mem_requirements = max((self.max_consumer_lag * self.mean_msg_size) / MILLION,
                                             FLUSH_DELAY_SECONDS * per_partition_produce_rate_mbps)
        ebs_bw_requirement = per_partition_produce_rate_mbps + self.num_replays * per_partition_replay_rate
        network_in_requirement = per_partition_produce_rate_mbps
        network_out_requirement = (self.num_consumers + self.replication_factor - 1) * \
                                  per_partition_produce_rate_mbps + self.num_replays * per_partition_replay_rate
        for p in range(self.num_partitions):
            result.append(Partition(per_partition_mem_requirements, network_in_requirement, network_out_requirement,
                                    ebs_bw_requirement, self.name, p, 0))
            for r in range(self.replication_factor - 1):
                result.append(Partition(per_partition_mem_requirements, network_in_requirement, network_out_requirement,
                                    ebs_bw_requirement, self.name, p, r + 1))
        return result


class Partition(ConstrainedItem):
    def __init__(self, memory, network_in, network_out, ebs_bw, topic, pid, rid):
        super(Partition, self).__init__([memory, ebs_bw, network_in, network_out])
        self.memory = memory
        self.network_in = network_in
        self.network_out = network_out
        self.ebs_bw = ebs_bw
        self.topic = topic
        self.pid = pid
        self.rid = rid

    def __repr__(self):
        return str([self.requirements, self.topic, self.pid, self.rid])

    def is_constraint_satisfied(self, broker):
        for item in broker.items:
            if item.pid == self.pid:
                return False
        return True


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
        self.node_types = sorted(node_types, key=lambda n: n.vcpus)
        self.workload = workload

    def find_bin_lower_bound(self):
        partitions = self.workload.partitions()
        max_network_out = max(partitions, key=lambda p: p.network_out).network_out
        max_network_in = max(partitions, key=lambda p: p.network_in).network_in
        max_ebs_bw = max(partitions, key=lambda p: p.ebs_bw).ebs_bw
        max_mem = max(partitions, key=lambda p: p.memory).memory

        for i, n in enumerate(self.node_types):
            if n.memory > max_mem and n.network_bw > max_network_in and n.network_bw > max_network_out and n.ebs_bw > max_ebs_bw:
                return i

    def plan(self):
        best_cost = sys.maxint
        best_instance = None
        best_config = None
        lb = self.find_bin_lower_bound()
        best_instance = self.node_types[lb]
        for i in range(lb, len(self.node_types)):
            node = self.node_types[i]
            assignment = optimize(self.workload.partitions(), node)
            cost = len(assignment.bins) * node.cost
            if cost < best_cost:
                best_cost = cost
                best_instance = node
                best_config = assignment

        return best_config, best_instance



