from fio import *
from jinja2 import Environment as JinjaEnvironment
from math import ceil
import os
import logging
import csv
import sys
import yaml
import tempfile
import time


BLOCK_SIZES = ["64k", "128k", "256k", "512k", "1024k"]
WRITE_MIXES = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
TOTAL_LOGS = [1, 2, 4, 8, 12, 16, 20]
LEADER_LOGS = [100, 70, 50, 30]
NUM_FILES_TO_FILESIZE_MAPPING = ["1G", "512m", "384m", "256m", "128m", "64m", "64m", "64m"]
FILE_SIZE = 1  # 2 gigabytes
POISSON_RATE_PROCESS = "poisson"

template_src = """\
[global]
group_reporting
bs=${block_size}
directory=${directory}
direct=1
io_submit_mode=offload
rate_process=${rate_process}
filesize=${filesize}

[kafka-sim-lead-replicas]
rw=rw
rwmixwrite=${write_pct}
nrfiles=${num_leaders}

{% if num_followers > 0 %}
[kafka-sim-follower-replicas]
rw=write
nrfiles=${num_followers}
{% endif %}\
"""

fio_job_template = JinjaEnvironment(
    line_statement_prefix='%',
    variable_start_string="${",
    variable_end_string="}"
).from_string(template_src)


def delete_folder_content(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            logging.error('Could not delete file ' + file_path, e)


def run_bench(bsizes, wmixes, tlogs, llogs, directory, rate_process, fio_path, result_file):
    with open(result_file, 'wb') as r:
        field_names = ['block_size', 'write_pct', 'leaders', 'followers', 'rate_process', 'iops', 'read_iops',
                       'read_latency', 'write_latency', 'read_tpt', 'write_tpt', 'total_writes']
        result_writer = csv.DictWriter(r, fieldnames=field_names)
        result_writer.writeheader()

        for bs in bsizes:
            for wm in wmixes:
                for tl in tlogs:
                    for ll in llogs:
                        leaders = int(ceil(tl * (ll / 100.0)))
                        followers = tl - leaders
                        file_size = "1G"

                        if tl < 9:
                            file_size = NUM_FILES_TO_FILESIZE_MAPPING[tl - 1]
                        else:
                            file_size = "32m"                            

                        tmp_dir = "{}/{}".format(tempfile.gettempdir(), 'csbench')
                        if not os.path.exists(tmp_dir):
                            os.makedirs(tmp_dir)

                        job_file = "{}/{}-{}-{}-{}-{}-{}-{}.ini".format(tmp_dir, bs, wm, tl, leaders, followers, file_size,
                                                                     rate_process)
                        with open(job_file, 'w') as f:
                            f.write(fio_job_template.render({
                                'block_size': bs,
                                'directory': directory,
                                'rate_process': rate_process,
                                'write_pct': wm,
                                'num_leaders': leaders,
                                'num_followers': followers,
                                'filesize': file_size
                            }))

                        print 'Created fio job file:', job_file 

                        fio_job = FIOJob(job_file, fio_path)
                        fio_job.run()
                        output = {
                            'block_size': bs, 'write_pct': wm, 'leaders': leaders, 'followers': followers,
                            'rate_process': rate_process, 'iops': fio_job.get_iops(),
                            'read_iops': fio_job.get_read_iops(),
                            'read_latency': fio_job.get_read_latency()[2],
                            'write_latency': fio_job.get_write_latency()[2], 'read_tpt': fio_job.get_read_throughput(),
                            'write_tpt': fio_job.get_write_throughput(), 'total_writes': fio_job.get_total_write_io()
                        }
                        result_writer.writerow(output)
                        r.flush()
                        delete_folder_content(directory)  # cleaning up data directory
                        time.sleep(10)

if __name__ == "__main__":
    # run_bench(["128k"], [60], [6], [50], '',
    #           POISSON_RATE_PROCESS, '/usr/local/bin/fio', 'fio-result.csv')
    if len(sys.argv) < 3:
        logging.error("Missing configuration file.")
        logging.error("Usage: python csbench.py config.yml")
        exit(-1)

    config = yaml.load(file(sys.argv[1], 'r'))
    run_bench(config['block-sizes'], config['write-mixes'], config['total-logs'], config['leader-logs'], config['data-directory'],
              config['rate-process'], config['fio-path'], sys.argv[2])
