from planner import Topic, LogStoreWorkload, LogStoreCapacityPlanner
from aws import InstanceType, StorageType, InstanceBin
import sys
import logging
import random
import numpy as np

per_partition_arrival_rates_ = [100000, 200000, 250000, 300000, 350000]
per_partition_arrival_rates = [100000, 200000, 250000]
message_sizes_ = [150, 250, 300]
message_sizes = [150, 250]
source_partition_counts = [20, 30, 40, 50]
replay_rate_multipliers_ = [3, 4, 5]
replay_rate_multipliers = [2]
consumer_lags = [20, 30, 40, 50]
intermediate_topics = [0, 1, 2, 3, 4]  # 0 intermediate topics simulate the processing of derived queries
inverse_query_parallelisms = [1, 2, 3, 4]
query_result_consumers = [1, 2]
bins = [InstanceBin(InstanceType.M4_2X, StorageType.ST1), InstanceBin(InstanceType.M4_4X, StorageType.ST1),
        InstanceBin(InstanceType.M4_10X, StorageType.ST1), InstanceBin(InstanceType.M4_16X, StorageType.ST1),
        InstanceBin(InstanceType.D2_2X, StorageType.D2HDD), InstanceBin(InstanceType.D2_4X, StorageType.D2HDD),
        InstanceBin(InstanceType.D2_8X, StorageType.D2HDD)]
bins_ = [InstanceBin(InstanceType.M4_2X, StorageType.ST1), InstanceBin(InstanceType.M4_4X, StorageType.ST1),
        InstanceBin(InstanceType.M4_10X, StorageType.ST1), InstanceBin(InstanceType.M4_16X, StorageType.ST1)]


def gen_workload(data_sources, realtime_queries, replay_queries, replication_factor, retention_period):
    # First generate data sources with random data rate, mean message size and partition count
    # Then generate queries in a way that there is at least one query reading each data source
    # Query can have multiple intermediate streams and a single output stream
    # Generate replay queries. replay can have multiple intermediate streams and one output streams
    # Each derive result is consumed by one or more consumers
    current_replays = 0
    workload = LogStoreWorkload()
    source_topics = []
    queries = []

    for i in range(0, data_sources):
        per_partition_arrival_rate = random.choice(per_partition_arrival_rates)
        mean_message_size = random.choice(message_sizes)
        source_partition_count = random.choice(source_partition_counts)

        replay = False
        if current_replays < replay_queries:
            replay = True
            current_replays += 1

        source_topics.append({
            'name': 'source-{}'.format(i),
            'arrival_rate': per_partition_arrival_rate * source_partition_count,
            'partition_count': source_partition_count,
            'mean_record_size': mean_message_size,
            'replay': replay,
            'replay_multiplier': random.choice(replay_rate_multipliers),
            'consumer_lag': random.choice(consumer_lags),
            'consumers': 0
        })

    for j in range(0, realtime_queries):
        source = random.choice(source_topics)
        itopics = random.choice(intermediate_topics)
        result_consumers = random.choice(query_result_consumers)
        source['consumers'] += 1
        queries.append({
            'name': 'query-{}'.format(j),
            'source': source,
            'intermediate_topics': itopics,
            'result_consumers': result_consumers
        })

    for st in source_topics:
        workload.add_topic(Topic(st['name'], st['arrival_rate'], st['mean_record_size'], st['partition_count'],
                                 replication_factor, st['consumers'], 1 if st['replay'] else 0,
                                 st['arrival_rate'] * st['replay_multiplier'], st['consumer_lag'], retention_period))

    for q in queries:
        source = q['source']
        itopics = q['intermediate_topics']
        result_consumers = q['result_consumers']
        source_partitions = source['partition_count']
        name = q['name']

        for j in range(0, itopics):
            workload.add_topic(Topic('{}-itopic-{}'.format(name, j), source['arrival_rate'], source['mean_record_size'],
                                     source_partitions, replication_factor,
                                     1 if j < itopics - 1 else result_consumers, 0, 0,
                                     random.choice(consumer_lags), retention_period))

    return workload


if __name__ == "__main__":
    # if len(sys.argv) < 6:
    #     logging.error('Not enough arguments.')
    #     exit(-1)
    #
    # workload = gen_workload(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    # print 'Partitions:', len(workload.partitions())
    # cp = LogStoreCapacityPlanner(bins, workload)
    # p = cp.plan()
    # print 'Bins:', len(p['assignment'].bins)
    # print 'Cost:', sum([b.hourly_cost() for b in p['assignment'].bins])

    workload = LogStoreWorkload()
    workload.add_topic(Topic("t1", 1000000, 254, 50, 2, 1, 0, 0, 50, 24))
    workload.add_topic(Topic("t1", 2000000, 178, 70, 2, 1, 0, 0, 45, 24))
    workload.add_topic(Topic("t1", 1500000, 334, 60, 2, 1, 0, 0, 50, 24))
    workload.add_topic(Topic("t1", 1500000, 234, 60, 2, 1, 1, 4500000, 50, 24))

    print 'Partition Count:', len(workload.partitions())

    cp = LogStoreCapacityPlanner(bins, workload)
    p = cp.plan()
    other_plans = p['other-plans']
    print 'Bin Type:', p['bin-type'].instance_type
    print 'Storage Bin Type:', p['bin-type'].storage_type
    print 'Bin Count:', len(p['assignment'].bins)
    print 'Naive Cost:', sum([b.hourly_cost() for b in p['assignment'].bins])
    max_util = []

    for b in p['assignment'].bins:
        if sum(b.utilization()) > 0:
            max_util.append(max(b.utilization()))
    print max_util
    print 'Mean Max Util:', np.mean(max_util)
    print 'STDEV Max Util:', np.std(max_util)
    print 'Utilization:'
    for b in p['assignment'].bins:
        if sum(b.utilization()) > 0:
            print b.utilization(), len(b.storage_bins), [1 if sb.num_logs > 0 else 0 for sb in b.storage_bins]

    print 'Alternative Plans:'
    for op in other_plans:
        print op[1].instance_type, op[1].storage_type, len(op[0].bins), op[2]
