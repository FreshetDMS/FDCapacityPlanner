from operator import truediv, sub
from enum import Enum, unique
from vsvbp.container import Bin
from math import ceil


@unique
class EC2InstanceType(Enum):
    M4_2X = 1
    M4_4X = 2
    M4_10X = 3
    M4_16X = 4

    def name(self):
        if self.value == 1:
            return "m4.2xlarge"
        elif self.value == 2:
            return "m4.4xlarge"
        elif self.value == 3:
            return "m4.10xlarge"
        elif self.value == 4:
            return "m4.16xlarge"

    def max_network_bw_mbps(self):
        if self.value == 1:
            return 118
        elif self.value == 2:
            return 237
        elif self.value == 3:
            return 1250
        elif self.value == 4:
            return 2500

    def max_dedicated_ebs_bw_mbps(self):
        if self.value == 1:
            return 125
        elif self.value == 2:
            return 250
        elif self.value == 3:
            return 500
        elif self.value == 4:
            return 1250

    def mem_gb(self):
        if self.value == 1:
            return 32
        elif self.value == 2:
            return 64
        elif self.value == 3:
            return 160
        elif self.value == 4:
            return 256

    def hourly_cost(self):
        if self.value == 1:
            return 0.296
        elif self.value == 2:
            return 0.592
        elif self.value == 3:
            return 1.480
        elif self.value == 4:
            return 2.369

    def __repr__(self):
        return str([self.name(), self.mem_gb(), self.max_dedicated_ebs_bw_mbps(), self.max_network_bw_mbps()])


# Max per volume throughput changes for some volumes based on the allocated volume size. In the context of capacity
# we consider max possible throughput and adjust the volume size to fit logs allocated to each bin and their storage
# requirements. Furthermore, for volume types such as st1 and instance HDD measured throughput is lower than max
# throughput. Also EBS throughput is limited by dedicated EBS bandwidth as well. So we should figure out per volume
# throughput values and total possible EBS throughput for each instance type empirically.
@unique
class AWSInstanceStorageType(Enum):
    IO1 = 1
    GP2 = 2
    ST1 = 3
    HDD = 4

    def get_size(self):
        return -1

    def get_iops(self, io_size_kb, ebs_bw):
        return -1

    def predict_effective_iops(self, io_size_kb, ebs_bw, num_logs):
        return -2

    def per_volume_throughput_limit_mbps(self):
        if self.value == 1:
            return 320
        elif self.value == 2:
            return 160
        elif self.value == 3:
            return 500
        elif self.value == 4:
            return 100

    def predict_capacity_in_iops(self, io_size, instance_type, num_logs):
        """
        Overall throughput of EBS volumes of type st1 that uses HDDs get reduced as the I/O requests become random and 
        average size of a I/O operation in less than ideal IO operation size. Here we predict the overall throughput as 
        a function of I/O operation size, EC2 instance type and number of files frequently accessed from the volume.
        
        :param io_size: Mean size of a single IO operation
        :param instance_type: EC2 instance type
        :param num_logs: Number of logs accessed (read/write) simultaneously
        :return: overall throughput
        """
        # Assumes max possible IOPS/Throughput volume
        if self.value == 1:
            return self.predict_io1_throughput(io_size, instance_type, num_logs)
        elif self.value == 2:
            return self.predict_gp2_throughput(io_size, instance_type, num_logs)
        elif self.value == 3:
            return self.predict_st1_throughput(io_size, instance_type, num_logs)
        elif self.value == 4:
            return self.predict_hdd_throughput(io_size, instance_type, num_logs)

    def predict_st1_throughput(self, io_size, instance_type, num_logs):
        # TODO: Fix this to include regression based prediction
        return instance_type.max_dedicated_ebs_bw_mbps() \
            if instance_type.max_dedicated_ebs_bw_mbps() < self.per_volume_throughput_limit_mbps() \
            else self.per_volume_throughput_limit_mbps()

    def predict_io1_throughput(self, io_size, instance_type, num_logs):
        # Assumes random access does not reduce overall volume throughput
        return instance_type.max_dedicated_ebs_bw_mbps() \
            if instance_type.max_dedicated_ebs_bw_mbps() < self.per_volume_throughput_limit_mbps() \
            else self.per_volume_throughput_limit_mbps()

    def predict_gp2_throughput(self, io_size, instance_type, num_logs):
        # Assumes random access does not reduce overall volume throughput
        return instance_type.max_dedicated_ebs_bw_mbps() \
            if instance_type.max_dedicated_ebs_bw_mbps() < self.per_volume_throughput_limit_mbps() \
            else self.per_volume_throughput_limit_mbps()

    def predict_hdd_throughput(self, io_size, instance_type, num_logs):
        return 100

    def hourly_cost(self, size_gb, provisioned_iops):
        hourly_cost_factor = 1.0 / (24 * 30)
        monthly_cost = 0

        if self.value == 1:
            monthly_cost = 0.125 * size_gb + 0.065 * provisioned_iops
        elif self.value == 2:
            monthly_cost = 0.10 * size_gb
        elif self.value == 3:
            monthly_cost = 0.045 * size_gb
        elif self.value == 4:
            monthly_cost = 0

        return monthly_cost * hourly_cost_factor


class StorageVolume(object):
    def __init__(self, storage_type, instance_type, io_size_kb):
        # TODO: Add storage capacity to this. Storage capacity can be calculated if we know retention period
        self.num_logs = 0
        self.storage_type = storage_type
        self.instance_type = instance_type
        self.io_size_kb = io_size_kb
        self.initial_capacity = storage_type.get_capacity()
        self.capacity_of_items = 0

    def add_log(self, capacity_req):
        self.num_logs += 1
        self.capacity_of_items += capacity_req

    def will_this_item_fit(self, item_capacity_req):
        # TODO: Check capacity ass well
        return self.remaining_capacity() > item_capacity_req

    def remaining_capacity(self):
        # TODO: Return remaining capacity as well
        return self.storage_type.predict_effective_capacity(self.instance_type, self.io_size_kb, self.num_logs + 1) - \
               self.capacity_of_items


# TODO: Apply the same logic applied above to calculate remaining capacity for the instance.
# TODO: Since BFD checks remaining directly this is little bit complicated. We can't pack logs that require more
# TODO: capacity than left in any single volume. Having bandwidth is not enough.
# TODO: log should fit into a volume. May be report the remaining of max remaining value from all volumes/disks
# TODO: Item should have storage capacity as a dimension too
class EC2Instance2(Bin):
    def __init__(self, instance_type, storage_type, ioop_size_kb=128):
        super(EC2Instance2, self).__init__(EC2Instance2.compute_initial_capacity(instance_type, storage_type,
                                                                                 ioop_size_kb))
        self.instance_type = instance_type
        self.storage_type = storage_type
        self.ioop_size_kb = ioop_size_kb
        self.volumes = [StorageVolume(storage_type, instance_type, ioop_size_kb) for i in
                        range(EC2Instance2.compute_initial_volume_count(instance_type, storage_type, ioop_size_kb))]
        self.last_volume_selected = -1

    @classmethod
    def compute_initial_volume_count(cls, instance_type, storage_type, ioop_size_kb):
        # IOPS based calculation
        return int(ceil(((instance_type.max_dedicated_ebs_bw_mbps() * 1024.0) / ioop_size_kb) /
                        storage_type.predict_capacity_in_iops(ioop_size_kb, instance_type, 1)))

    @classmethod
    def compute_initial_capacity(cls, instance_type, storage_type, ioop_size_kb):
        return [instance_type.mem_gb(), min(instance_type.max_dedicated_ebs_bw_mbps(),
                                            storage_type.predict_capacity_in_iops(ioop_size_kb, instance_type, 1)),
                instance_type.max_network_bw_mbps(), instance_type.max_network_bw_mbps()]

    def __repr__(self):
        return str([self.instance_type, self.storage_type, self.ioop_size_kb, self.remaining])

    def select_volume(self, capacity_req):
        # Implements best fit selection. Selects the smallest feasible bin.
        for sv in sorted(self.volumes, key=lambda v: v.remaining_capacity()):
            if sv.remaining_capacity() > capacity_req:
                return sv
        return None  # Return none if no disk/volume can accommodate the log

    def insert(self, item):
        storage_selection = self.select_volume(item.requirements[1])  # TODO: Do we need to consider disk space
        # While general bin capacity calculation ignores index of capacity array, we can't do this here since we need
        # to dynamically update the overall capacity of EBS volumes
        for i, req in enumerate(item.requirements):
            if i == 1:
                self.remaining[i] = self.compute_remaining_storage_capacity(current_volume_selected, self.remaining[i],
                                                                            req)
            else:
                self.remaining[i] -= req

        self.items.append(item)

        self.last_volume_selected = current_volume_selected

    def compute_remaining_storage_capacity(self, current_vol, remaining, cur_req):
        remaining_capacity = 0
        for i, vol in enumerate(self.volumes):
            if i == current_vol:
                remaining_capacity += 100
            else:
                pass
        # We don't need to calculate everything. Just remove the current selected vols capacity from remaning, calculate
        # new capacity of current selected vol and negate item requirement
        return remaining_capacity

    def vol_count(self):
        return len(self.volumes)


class EC2Instance(Bin):
    def __init__(self, instance_type, vcpus, memory, network_bw, ebs_bw, cost):
        super(EC2Instance, self).__init__([memory, ebs_bw, network_bw, network_bw])
        self.memory = memory
        self.ebs_bw = ebs_bw
        self.network_bw = network_bw
        self.instance_type = instance_type
        self.vcpus = vcpus
        self.cost = cost

    def __repr__(self):
        return str([self.instance_type, self.vcpus, self.capacities, self.remaining])

    def utilization(self):
        return map(truediv, map(sub, self.capacities, self.remaining), self.capacities)
