from vsvbp.container import ConstrainedItem
import logging

logger = logging.getLogger("fdcp")


class Partition(ConstrainedItem):
    def __init__(self, memory, network_in, network_out, ebs_bw, reads, topic, pid, rid):
        super(Partition, self).__init__([memory, ebs_bw, network_in, network_out])
        self.memory = memory
        self.network_in = network_in
        self.network_out = network_out
        self.ebs_bw = ebs_bw
        self.reads = reads
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

    def is_leader(self):
        return self.rid == 0



