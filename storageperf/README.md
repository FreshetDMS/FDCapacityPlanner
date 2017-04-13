# AWS Storage Performance Modeling

This directory contains a set of [fio](http://fio.readthedocs.io/en/latest/) based micro-benchmarks for measuring performance (IOPS/throughput) of different AWS storage offerings under different conditions (multiple I/O operation sizes and simultaneous access of multiple files) for performance modeling purposes.  

# Basic Model

A black-box model that predicts the performance as a function (F) of workload characteristics (wc).

```math
p = F(wc)
```

We are interested in throughput in IOs per second. So *p* is IOPS. *F* will be derived as a decision tree model. We can characterized the AWS storage workloads by read and write ratio (*rw_ratio*), IO operation size (*io_size*) assuming both read and write requests are of same size, queue depth (*q_dep*) that represents the number of outstanding I/Os, and read and write request randomness (*r_rand, w_rand*).

```math
wc = <rw_ratio, q_dep, io_size, r_rand, w_rand> 
```

# Workload Generation

We use [fio](http://fio.readthedocs.io) for workload generation. When a parameter is not being analyzed, the default values are shown below.

```
+=--------------+-------------+------------+-----------+-----------------+------------------+
| write_ratio   | queue_depth | write_size | read_size | read_randomness | write_randomness |
+===============+=============+============+===========+=================+==================+
| 0(RO),100(WO) | 1           | 256KB      | 256 KB    | 1               | 1                |
+---------------+-------------+------------+-----------+-----------------+------------------+
```

## FIO Tips and Tricks

* Use ```ramp_time``` to delay metric collection to get more stable results
* Consider using ```loops``` and ```numjobs```
* Can we use ```nrfiles``` to simulate random access, instead of ```numjobs```
* Investigate the effect of ```file_service_type```
* ```unified_rw_reporting``` can be used to get aggregated results for reads, writes and trims
* Try to log the history and verify the workload generation