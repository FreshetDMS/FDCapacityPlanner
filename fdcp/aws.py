from enum import Enum
from fdcp import Partition
from math import ceil
from vsvbp.container import Bin

INSTANCE_MODEL_LIST = ["m4.2xlarge", "m4.4xlarge", "m4.10xlarge", "m4.16xlarge", "d2.2xlarge", "d2.4xlarge",
                       "d2.8xlarge"]
INSTANCE_MEM_LIST = [32, 64, 160, 256, 61, 122, 244]
INSTANCE_NETWORK_BW_LIST = [118, 237, 1250, 2500, 118, 237, 1250]
INSTANCE_STORAGE_BW_LIST = [125, 250, 500, 1250, 875, 1750, 3500]
INSTANCE_HOURLY_COST_LIST = [0.296, 0.592, 1.480, 2.369, 0.804, 1.608, 3.216]

STORAGE_MODEL_LIST = ["io1", "gp2", "st1", "d2hdd"]
STORAGE_SIZE_LIST = [16, 16, 16, 2]
STORAGE_HOURLY_COST_FACTOR = 1.0 / (24 * 30)
STORAGE_HOURLY_COST = [lambda (size, iops): 0.125 * size + 0.065 * iops, lambda (size, iops): 0.10 * size,
                       lambda (size, iops): 0.045 * size, lambda (size, iops): 0]

KBS_TO_MB = 1024


class InstanceType(Enum):
    M4_2X = 1
    M4_4X = 2
    M4_10X = 3
    M4_16X = 4
    D2_2X = 5
    D2_4X = 6
    D2_8X = 7

    def model(self):
        return INSTANCE_MODEL_LIST[self.value - 1]

    def memory(self):
        return INSTANCE_MEM_LIST[self.value - 1]

    def network_bandwidth(self):
        return INSTANCE_NETWORK_BW_LIST[self.value - 1]

    def storage_bandwidth(self):
        return INSTANCE_STORAGE_BW_LIST[self.value - 1]

    def hourly_cost(self):
        return INSTANCE_HOURLY_COST_LIST[self.value - 1]


class StorageType(Enum):
    IO1 = 1
    GP2 = 2
    ST1 = 3
    D2HDD = 4

    def model(self):
        return STORAGE_MODEL_LIST[self.value - 1]

    def size(self):
        return STORAGE_SIZE_LIST[self.value - 1]

    def iops(self, io_op_size_kb, storage_bw):
        # Predicted IOPS assuming there is only no random io
        # Things to consider
        #   - Max IOPS change with the I/O operation size
        # We need to collect data for each storage type
        # Storage Type | 64 KB | 128 KB | 256 KB | 512 KB | 1MB
        # io1          |       |        |        |        |
        # gp2          |       |        |        |        |
        # st1          |       |        |        |        |
        # hdd          |       |        |        |        |
        pass

    def effective_iops(self, io_op_size_kb, storage_bw, reads_pct, rand_factor):
        # Do we need to consider total storage bandwidth or remaining bandwidth? I think total because effective
        # bandwidth is limited by dedicated storage bandwidth
        # We need to collect data for all the storage types for io size and number of logs
        # io size | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10  <-- num logs
        #  64KB   |
        # 128KB   |
        # 256KB   |
        #   ...   |
        #   1MB   |
        pass

    def hourly_cost(self, size, provisioned_iops):
        return STORAGE_HOURLY_COST_FACTOR * STORAGE_HOURLY_COST[self.value - 1](size, provisioned_iops)


class StorageBin(object):
    def __init__(self, storage_type, instance_type, io_op_size_kb):
        self.storage_type = storage_type
        self.instance_type = instance_type
        self.io_op_size_kb = io_op_size_kb
        self.num_logs = 0
        self.capacity = []
        self.remaining = []
        self.capacity_of_items = []
        self.reads = 0

    def add_item(self, item, read_pct):
        """
        Add a new item to storage bin.
        :param item: array representing IOPS and space requirements [size_req, iops_req]
        :param read_pct: Reads as a percentage of total IOPS requirement
        :return: None
        """
        self.num_logs += 1
        self.capacity_of_items = [x + y for x, y in zip(self.capacity_of_items, item)]
        self.reads += item[1] * read_pct
        self.remaining = [self.storage_type.size() - self.capacity_of_items[0],
                          self.effective_iops() - self.capacity_of_items[1]]

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
        total_read_pct = float(self.reads) / self.capacity_of_items[1]
        return self.storage_type.effective_iops(self.io_op_size_kb, self.instance_type.storage_bandwidth(),
                                                total_read_pct, self.num_logs + 1)

    def effective_throughput(self):
        return self.effective_iops() * self.io_op_size_kb


class InstanceBin(Bin):
    def __init__(self, instance_type, storage_type, io_op_size_kb=128):
        super(InstanceBin, self).__init__(
            InstanceBin.compute_initial_capacity(instance_type, storage_type, io_op_size_kb))
        self.instance_type = instance_type
        self.storage_type = storage_type
        self.io_op_size_kb = io_op_size_kb
        self.storage_bins = [StorageBin(storage_type, instance_type, io_op_size_kb) for i in
                             range(InstanceBin.compute_volume_count(instance_type, storage_type, io_op_size_kb))]

    def insert(self, item):
        sb = self.select_storage_bin(item.requirements[1], item.requirements[2])
        if sb is None:
            # There is a possibility of adding a new storage bin and adjusting remaining storage bw as needed.
            # But if storage capacity is not enough going to the next bin may be the solution
            raise Exception('Storage capacity requirements exceed remaining storage capacity.')

        sb.add_item([item.requirements[1], item.requirements[2]], item.reads)

        self.allocate_new_storage_bins_if_necessary()

        for i, req in enumerate(item.requirements):
            if i != 1 and i != 2:
                self.remaining[i] -= req

        max_sb = next(iter(sorted(self.storage_bins, key=lambda sbin: sbin.vector_sum_of_remaining(), reverse=True)),
                      None)
        if max_sb is None:
            raise Exception('Storage bin with max remaining capacity cannot be none.')

        self.remaining[1] = max_sb.remaining[0]
        self.remaining[2] = max_sb.remaining[1]

        self.items.append(item)

    def add(self, item):
        if not isinstance(item, Partition):
            raise Exception('Only items of type Partition is supported at this stage.')

        if self.feasible(item):
            self.insert(item)
            return True
        return False

    def allocate_new_storage_bins_if_necessary(self):
        # We can do this because effective throughput goes down as we add more logs to storage bin
        effective_storage_throughput = sum(sb.effective_throughput() for sb in self.storage_bins)
        if effective_storage_throughput < self.instance_type.storage_bandwidth():
            self.storage_bins.append(StorageBin(self.storage_type, self.instance_type, self.io_op_size_kb))

    def storage_bin_count(self):
        return len(self.storage_bins)

    # Private methods
    def select_storage_bin(self, size_req, iops_req):
        for sb in sorted(self.storage_bins, key=lambda sbin: sbin.vector_sum_of_remaining()):
            if sb.feasible([size_req, iops_req]):
                return sb
        return None

    @classmethod
    def compute_initial_capacity(cls, instance_type, storage_type, io_op_size_kb):
        return [instance_type.memory(), storage_type.size(),
                storage_type.iops(io_op_size_kb, instance_type.storage_bandwidth()),
                instance_type.network_bandwidth(), instance_type.network_bandwidth()]

    @classmethod
    def compute_volume_count(cls, instance_type, storage_type, io_op_size_kb):
        return int(ceil(((instance_type.storage_bandwidth() * KBS_TO_MB) / io_op_size_kb) /
                        storage_type.iops(io_op_size_kb,
                                          instance_type.storage_bandwidth())))
