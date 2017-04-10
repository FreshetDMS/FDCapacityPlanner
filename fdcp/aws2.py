from enum import Enum
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
        pass

    def effective_iops(self, io_op_size_kb, storage_bw, rand_factor):
        # Do we need to consider total storage bandwidth or remaining bandwidth? I think total because effective
        # bandwidth is limited by dedicated storage bandwidth
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

    def add_item(self, item):
        """
        Add a new item to storage bin.
        :param item: array representing IOPS and space requirements [size_req, iops_req]
        :return: None
        """
        self.num_logs += 1
        self.capacity_of_items = [x + y for x, y in zip(self.capacity_of_items, item)]
        self.remaining = [self.storage_type.size() - self.capacity_of_items[0],
                          self.storage_type.effective_iops(self.io_op_size_kb, self.instance_type.storage_bandwidth(),
                                                           self.num_logs + 1) - self.capacity_of_items[1]]

    def feasible(self, item):
        for i, c in enumerate(item):
            if c > self.remaining[i]:
                return False
        return True

    def vector_sum_of_remaining(self):
        return sum(self.remaining)


class InstanceBin(Bin):
    def __init__(self, instance_type, storage_type, io_op_size_kb=128):
        super(InstanceBin, self).__init__(
            InstanceBin.compute_initial_capacity(instance_type, storage_type, io_op_size_kb))
        self.instance_type = instance_type
        self.storage_type = storage_type
        self.io_op_size_kb = io_op_size_kb
        self.storage_bins = [StorageBin(storage_type, instance_type, io_op_size_kb) for i in
                             range(InstanceBin.compute_volume_count())]

    def insert(self, item):
        # Select storage bin
        # Insert item
        # Check whether effective capacity of storage bins went below effective bandwidth allocated for storage and
        # add more storage bins.
        # Calculate remaining capacity
        # Report both size as well as iops for storage
        pass

    def storage_bin_count(self):
        return len(self.storage_bins)

    # Private methods
    def select_storage_bin(self, req):
        for sb in sorted(self.storage_bins, key=lambda sb: sb.vector_sum_of_remaining()):
            if sb.feasible(req):
                return sb
        return None

    def compute_remaining_capacity(self):
        pass

    @classmethod
    def compute_initial_capacity(cls, instance_type, storage_type, io_size_kb):
        return [instance_type.memory(), storage_type.size(),
                storage_type.iops(io_size_kb, instance_type.storage_bandwidth()),
                instance_type.network_bandwidth(), instance_type.network_bandwidth()]

    @classmethod
    def compute_volume_count(cls):
        return 0
