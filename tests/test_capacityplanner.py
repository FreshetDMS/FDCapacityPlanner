from fdcp import *
import unittest


class LogStoreCapacityPlannerTestCase(unittest.TestCase):
    def setUp(self):
        self.node_types = [EC2Instance("m4.xlarge", 4, 16 * 1024, 125, 750 / 8, 1),
                           EC2Instance("m4.2xlarge", 8, 32 * 1024, 125, 1000 / 8, 2),
                           EC2Instance("m4.4xlarge", 16, 64 * 1024, 125, 2000 / 8, 4),
                           EC2Instance("m4.10xlarge", 40, 160 * 1024, 1250, 4000 / 8, 10),
                           EC2Instance("m4.16xlarge", 64, 256 * 1024, 2500, 10000 / 8, 16)]

    def testSimple(self):
        workload = LogStoreWorkload()
        workload.add_topic(Topic("t1", MILLION * 2, 112, 100, 2, 2, 1, MILLION * 3, 10))
        workload.add_topic(Topic("t2", int(MILLION * 1.5), 198, 150, 3, 4, 1, int(MILLION * 2.5), 20))
        workload.add_topic(Topic("t3", int(MILLION * 0.5), 398, 75, 1, 4, 1, int(MILLION * 1.5), 30))
        cp = LogStoreCapacityPlanner(self.node_types, workload)
        assignment, node_type = cp.plan()
        assert node_type.type == "m4.xlarge"
        assert len(assignment.bins) > 0
