from enum import Enum
from . import Partition
from math import ceil
from sklearn.externals import joblib
from vsvbp.container import Bin
import os
import numpy as np
import uuid
import logging

INSTANCE_MODEL_LIST = ["m4.2xlarge", "m4.4xlarge", "m4.10xlarge", "m4.16xlarge", "d2.2xlarge", "d2.4xlarge",
                       "d2.8xlarge"]
INSTANCE_CPU_LIST = [8, 16, 40, 64, 8, 16, 36]
INSTANCE_MEM_LIST = [32 * 1024, 64 * 1024, 160 * 1024, 256 * 1024, 61 * 1024, 122 * 1024, 244 * 1024]
INSTANCE_NETWORK_BW_LIST = [118, 237, 1250, 2500, 118, 237, 1250]
INSTANCE_STORAGE_BW_LIST = [125, 250, 500, 1250, 550, 550, 550]
INSTANCE_HOURLY_COST_LIST = [0.296, 0.592, 1.480, 2.369, 0.804, 1.608, 3.216]
INSTANCE_DISK_COUNT = [0, 0, 0, 0, 6, 12, 24]

STORAGE_MODEL_LIST = ["io1", "gp2", "st1", "d2hdd", "st1.static", "d2hdd.static"]
STORAGE_SIZE_LIST = [16 * 1024.0 * 1024.0, 16 * 1024.0 * 1024.0, 16 * 1024.0 * 1024.0, 2 * 1024.0 * 1024.0,
                     16 * 1024.0 * 1024.0, 2 * 1024.0 * 1024.0]
STORAGE_HOURLY_COST_FACTOR = 1.0 / (24 * 30)
STORAGE_HOURLY_COST = [lambda size, iops: 0.125 * size + 0.065 * iops, lambda size, iops: 0.10 * size,
                       lambda size, iops: 0.045 * size, lambda size, iops: 0, lambda size, iops: 0.045 * size,
                       lambda size, iops: 0]

MBS_TO_KB = 1024

# Does not support different io sizes. These models are for 128KB io operations
HDD_IOPS_MODEL = joblib.load(os.path.join(os.path.dirname(__file__), 'models/hdd.pkl'))
ST1_IOPS_MODEL = joblib.load(os.path.join(os.path.dirname(__file__), 'models/st1.pkl'))


class InstanceType(Enum):
    M4_2X = 1
    M4_4X = 2
    M4_10X = 3
    M4_16X = 4
    D2_2X = 5
    D2_4X = 6
    D2_8X = 7

    def __repr__(self):
        return str(self.model())

    def model(self):
        return INSTANCE_MODEL_LIST[self.value - 1]

    def vcpus(self):
        return INSTANCE_CPU_LIST[self.value - 1]

    def memory(self):
        return INSTANCE_MEM_LIST[self.value - 1]

    def network_bandwidth(self):
        return INSTANCE_NETWORK_BW_LIST[self.value - 1]

    def storage_bandwidth(self):
        return INSTANCE_STORAGE_BW_LIST[self.value - 1]

    def max_storage_size(self):
        if self.value == 1 or self.value == 2 or self.value == 3 or self.value == 4:
            return 16 * 1024.0 * 1024.0
        else:
            return 2 * 1024.0 * 1024.0

    def hourly_cost(self):
        return INSTANCE_HOURLY_COST_LIST[self.value - 1]

    def disk_count(self):
        return INSTANCE_DISK_COUNT[self.value - 1]


class StorageType(Enum):
    IO1 = 1
    GP2 = 2
    ST1 = 3
    D2HDD = 4
    ST1STATIC = 5
    D2HDDSTATIC = 6

    def __repr__(self):
        return str(self.model())

    def model(self):
        return STORAGE_MODEL_LIST[self.value - 1]

    def size(self):
        return STORAGE_SIZE_LIST[self.value - 1]

    def iops(self, io_op_size_kb, storage_bw):
        # Predicted IOPS assuming there is only no random io
        # Things to consider
        #   - Max IOPS change with the I/O operation size
        if self.value == 4:
            return min(HDD_IOPS_MODEL.predict([[1, 0, 50]])[0], (storage_bw * 1024.0) / io_op_size_kb)
        elif self.value == 3:
            return min(ST1_IOPS_MODEL.predict([[1, 0, 50]])[0], (storage_bw * 1024.0) / io_op_size_kb)
        elif self.value == 5:
            return min(ST1_IOPS_MODEL.predict([[1, 0, 50]])[0], (storage_bw * 1024.0) / io_op_size_kb)
        elif self.value == 6:
            return min(HDD_IOPS_MODEL.predict([[1, 0, 50]])[0], (storage_bw * 1024.0) / io_op_size_kb)
        else:
            return -1

    def effective_iops(self, io_op_size_kb, storage_bw, leaders, followers, write_pct):
        # Do we need to consider total storage bandwidth or remaining bandwidth? I think total because effective
        # bandwidth is limited by dedicated storage bandwidth
        # We need to collect data for all the storage types for io size and number of logs
        if self.value == 4:
            return min(HDD_IOPS_MODEL.predict([[leaders, followers, write_pct]])[0],
                       (storage_bw * 1024.0) / io_op_size_kb)
        elif self.value == 3:
            return min(ST1_IOPS_MODEL.predict([[leaders, followers, write_pct]])[0],
                       (storage_bw * 1024.0) / io_op_size_kb)
        elif self.value == 5:
            return min(ST1_IOPS_MODEL.predict([[1, 0, 50]])[0], (storage_bw * 1024.0) / io_op_size_kb)
        elif self.value == 6:
            return min(HDD_IOPS_MODEL.predict([[1, 0, 50]])[0], (storage_bw * 1024.0) / io_op_size_kb)
        else:
            raise RuntimeError("Effective iops calculation is not support for storage type: " + self.model())

    def hourly_cost(self, size, provisioned_iops, io_op_size_kb):
        # Cost calculation for EBS instances should find minimum size required to provide the said IOPS and then decide
        # cost based on that
        dr = io_op_size_kb * provisioned_iops

        if self.value == 3 or self.value == 5:
            if dr < 20:
                nsize = 0.5 * 1000
            elif dr < 40:
                nsize = 1 * 1000
            elif dr < 80:
                nsize = 2 * 1000
            elif dr < 120:
                nsize = 3 * 1000
            elif dr < 160:
                nsize = 4 * 1000
            elif dr < 200:
                nsize = 5 * 1000
            elif dr < 240:
                nsize = 6 * 1000
            elif dr < 280:
                nsize = 7 * 1000
            elif dr < 320:
                nsize = 8 * 1000
            elif dr < 360:
                nsize = 9 * 1000
            elif dr < 400:
                nsize = 10 * 1000
            elif dr < 440:
                nsize = 11 * 1000
            elif dr < 480:
                nsize = 12 * 1000
            else:
                nsize = 12.5 * 1000

            if size < nsize:
                size = nsize

        return STORAGE_HOURLY_COST_FACTOR * STORAGE_HOURLY_COST[self.value - 1](size, provisioned_iops)


class StorageBin(object):
    def __init__(self, storage_type, instance_type, io_op_size_kb, iid):
        self.iid = iid
        self.storage_type = storage_type
        self.instance_type = instance_type
        self.io_op_size_kb = io_op_size_kb
        self.num_logs = 0
        self.num_leaders = 0
        self.leader_total_io = 0
        self.leader_read_io = 0
        self.capacity = [self.storage_type.size(),
                         self.storage_type.iops(io_op_size_kb, instance_type.storage_bandwidth())]
        self.remaining = [self.storage_type.size(),
                          self.storage_type.iops(io_op_size_kb, instance_type.storage_bandwidth())]
        self.capacity_of_items = [0, 0]

    def __repr__(self):
        if self.num_leaders >= 1 and self.leader_read_io > 0:
            leader_write_pct = float(self.leader_total_io - self.leader_read_io) / self.leader_total_io
        elif self.leader_read_io == 0.0:
            leader_write_pct = 100
        else:
            leader_write_pct = 0
        return str({'logs': self.num_logs,
                    'leaders': self.num_leaders,
                    'remaining_capacity': self.remaining,
                    'capacity': self.capacity,
                    'type': self.storage_type,
                    'write_pct': leader_write_pct})

    def add_item(self, item, read_pct, leader=False):
        """
        Add a new item to storage bin.
        :param item: array representing IOPS and space requirements [size_req, iops_req]
        :param read_pct: Reads as a percentage of total IOPS requirement
        :return: None
        """
        self.num_logs += 1

        if leader:
            self.num_leaders += 1

        if read_pct > 0.0:  # In the context of prediction we consider partitions without reads as followers
            self.leader_total_io += item[1]
            self.leader_read_io += item[1] * read_pct

        self.capacity_of_items = [x + y for x, y in zip(self.capacity_of_items, item)]
        self.remaining = [self.storage_type.size() - self.capacity_of_items[0],
                          self.effective_iops() - self.capacity_of_items[1]]
        self.capacity[1] = self.effective_iops()

    def feasible(self, item):
        for i, c in enumerate(item):
            if c > self.remaining[i]:
                return False
        return True

    def vector_sum_of_remaining(self):
        # TODO: This is not a proper size measure since size is in thousands of giga bytes and bandwidth is in hundreds
        # TODO: of mega bytes. Fix this.
        return sum(self.remaining)

    def effective_iops(self):
        if self.num_leaders >= 1 and self.leader_read_io > 0.0:
            leader_write_pct = float(self.leader_total_io - self.leader_read_io) / self.leader_total_io
        if self.leader_read_io == 0.0:
            leader_write_pct = 100
        else:
            leader_write_pct = 0
        return self.storage_type.effective_iops(self.io_op_size_kb, self.instance_type.storage_bandwidth(),
                                                self.num_leaders, self.num_logs - self.num_leaders, leader_write_pct)

    def effective_throughput(self):
        return self.effective_iops() * self.io_op_size_kb

    def hourly_cost(self):
        return self.storage_type.hourly_cost(self.capacity_of_items[0] / (1024 * 1024), self.capacity_of_items[1],
                                             self.io_op_size_kb)


class InstanceBin(Bin):
    def __init__(self, instance_type, storage_type, io_op_size_kb=128):
        super(InstanceBin, self).__init__(
            InstanceBin.compute_initial_capacity(instance_type, storage_type, io_op_size_kb))
        self.bin_id = str(uuid.uuid4())
        self.instance_type = instance_type
        self.storage_type = storage_type
        self.io_op_size_kb = io_op_size_kb
        self.max_storage_bin_count = InstanceBin.compute_max_volume_count(instance_type, storage_type, io_op_size_kb)
        self.storage_bins = [StorageBin(storage_type, instance_type, io_op_size_kb, self.bin_id) for i in
                             range(InstanceBin.compute_volume_count(instance_type, storage_type, io_op_size_kb))]

    def insert(self, item):
        sb = self.select_storage_bin(item.requirements[1], item.requirements[2])
        if sb is None:
            # There is a possibility of adding a new storage bin and adjusting remaining storage bw as needed.
            # But if storage capacity is not enough going to the next bin may be the solution
            # logging.error('Storage capacity requirements exceed remaining storage capacity. Item: ' + str(item) +
            #               " Bin: " + str(self))
            return False

        leader = False
        if isinstance(item, Partition):
            leader = item.rid == 0

        sb.add_item([item.requirements[1], item.requirements[2]], item.reads, leader)

        self.allocate_new_storage_bins_if_necessary()

        for i, req in enumerate(item.requirements):
            if i != 1 and i != 2:
                self.remaining[i] -= req

        max_sb = self.max_sb_remaining()

        self.remaining[1] = max_sb.remaining[0]
        self.remaining[2] = max_sb.remaining[1]

        self.items.append(item)
        return True

    def max_sb_remaining(self):
        # If we are using EBS volumes, maximum remaining should be new vol capacity if current storage bin count is less
        # than max possible storage bin count
        max_sb = next(iter(sorted(self.storage_bins, key=lambda sbin: sbin.vector_sum_of_remaining(), reverse=True)),
                      None)
        if max_sb is None:
            raise Exception('Storage bin with max remaining capacity cannot be none.')

        if self.storage_bin_count() < self.max_storage_bin_count:
            return StorageBin(self.storage_type, self.instance_type, self.io_op_size_kb, self.bin_id)
        else:
            return max_sb

    def empty(self):
        super(InstanceBin, self).empty()
        self.storage_bins = [StorageBin(self.storage_type, self.instance_type, self.io_op_size_kb, self.bin_id) for i in
                             range(InstanceBin.compute_volume_count(self.instance_type, self.storage_type,
                                                                    self.io_op_size_kb))]

    def add(self, item):
        if not isinstance(item, Partition):
            raise Exception('Only items of type Partition is supported at this stage.')

        if self.feasible(item):
            return self.insert(item)
        return False

    def allocate_new_storage_bins_if_necessary(self):
        # We can do this because effective throughput goes down as we add more logs to storage bin
        if self.storage_type != StorageType.D2HDD and self.storage_bin_count() == self.max_storage_bin_count:
            effective_storage_throughput = sum(sb.effective_throughput() for sb in self.storage_bins)
            if effective_storage_throughput < self.instance_type.storage_bandwidth():
                self.storage_bins.append(
                    StorageBin(self.storage_type, self.instance_type, self.io_op_size_kb, self.bin_id))
                self.max_storage_bin_count += 1

    def storage_bin_count(self):
        return len(self.storage_bins)

    def hourly_cost(self):
        return self.instance_type.hourly_cost() + sum(
            [sb.hourly_cost() if sb.num_logs > 0 else 0 for sb in self.storage_bins])

    # Private methods
    def select_storage_bin(self, size_req, iops_req):
        for sb in sorted(self.storage_bins, key=lambda sbin: sbin.vector_sum_of_remaining()):
            if sb.feasible([size_req, iops_req]):
                return sb

        if self.storage_bin_count() < self.max_storage_bin_count:
            self.storage_bins.append(StorageBin(self.storage_type, self.instance_type, self.io_op_size_kb, self.bin_id))
        else:
            return None

        return self.select_storage_bin(size_req, iops_req)

    def utilization(self):
        total_storage_capacity = [0, 0]
        used_capacity = [0, 0]
        for sb in self.storage_bins:
            total_storage_capacity[0] += sb.capacity[0]
            total_storage_capacity[1] += sb.capacity[1]
            used_capacity[0] += sb.capacity_of_items[0]
            used_capacity[1] += sb.capacity_of_items[1]

        utilization = [float(c - r) / float(c) for c, r in zip(self.capacities, self.remaining)]
        utilization[1] = float(used_capacity[0]) / float(total_storage_capacity[0])
        utilization[2] = float(used_capacity[1]) / float(total_storage_capacity[1])
        return utilization

    def __repr__(self):
        return str({'type': self.instance_type,
                    'utilization': self.utilization(),
                    'capacity': self.capacities,
                    'remaining_capacity': self.remaining,
                    'storage_bins': self.storage_bins})

    @classmethod
    def compute_initial_capacity(cls, instance_type, storage_type, io_op_size_kb):
        if instance_type == InstanceType.D2_2X or instance_type == InstanceType.D2_4X or instance_type == InstanceType.D2_8X:
            iops = min(storage_type.iops(io_op_size_kb, instance_type.storage_bandwidth()) * instance_type.disk_count(),
                       (instance_type.storage_bandwidth() * MBS_TO_KB) / io_op_size_kb)
        else:
            iops = (instance_type.storage_bandwidth() * MBS_TO_KB) / io_op_size_kb

        return [instance_type.memory(),
                storage_type.size() * InstanceBin.compute_volume_count(instance_type, storage_type, io_op_size_kb),
                iops,
                instance_type.network_bandwidth(), instance_type.network_bandwidth()]

    @classmethod
    def compute_volume_count(cls, instance_type, storage_type, io_op_size_kb):
        if storage_type == StorageType.D2HDD or storage_type == StorageType.D2HDDSTATIC:
            return instance_type.disk_count()
        else:
            return 1

    @classmethod
    def compute_max_volume_count(cls, instance_type, storage_type, io_op_size_kb):
        if storage_type == StorageType.D2HDD or storage_type == StorageType.D2HDDSTATIC:
            return instance_type.disk_count()
        else:
            return int(ceil(((instance_type.storage_bandwidth() * MBS_TO_KB) / io_op_size_kb) /
                            storage_type.iops(io_op_size_kb,
                                              instance_type.storage_bandwidth())))
