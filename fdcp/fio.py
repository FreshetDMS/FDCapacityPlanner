import subprocess
import logging
import os

TERSE_READ_IOPS_POSITION = 7
TERSE_WRITE_IOPS_POSITION = 48
TERSE_TOTAL_IO_WRITE_POSITION = 46
TERSE_WRITE_LATENCY_START_POSITION = 78
TERSE_READ_LATENCY_START_POSITION = 37
TERSE_TOTAL_READ_THROUGHPUT_POSITION = 6
TERSE_TOTAL_WRITE_THROUGHPUT_POSITION = 47


def is_exe(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


class FIOJob(object):
    def __init__(self, config_path=None, fio_path=None, block_size="128k", group_reporting=True,
                 unified_reporting=False):
        self.config_path = config_path
        self.fio_path, self.fio_version = FIOJob.fio_path_and_version(fio_path)
        self.job_params = {}
        self.group_reporting = group_reporting
        self.unified_reporting = unified_reporting
        self.block_size = block_size
        self.success = False
        self.output = None
        self.terse_output = []

    def __repr__(self):
        return str([self.fio_path, self.fio_version, self.job_params, self.group_reporting, self.unified_reporting])

    def add_job_param(self, key, value):
        self.job_params[key] = value

    def prep_job_params(self):
        fio_args_list = []
        for k, v in self.job_params.iteritems():
            fio_args_list.append("--" + k + "=" + v)
        return fio_args_list

    def run(self):
        args = [self.fio_path, "--minimal"]

        if self.group_reporting:
            args.append("--group_reporting")

        if self.unified_reporting:
            args.append("--unified_rw_reporting=1")

        if self.config_path is None and not bool(self.job_params):
            args.extend(self.prep_job_params())
        elif self.config_path is not None:
            args.append(self.config_path)
        else:
            logging.error("Both fio configuration path and job parameters are empty.")
            raise RuntimeError("Empty fio configuration path and job parameters")

        logging.info(str(args))

        out = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = out.communicate()
        if stderr != '':
            logging.error("Error occurred while executing fio job: " + stderr)
            self.success = False
        else:
            self.success = True
            self.output = stdout
            self.terse_output = stdout.split(';')

    def get_iops(self):
        return int(self.terse_output[TERSE_READ_IOPS_POSITION]) + int(self.terse_output[TERSE_WRITE_IOPS_POSITION])

    def get_read_iops(self):
        return int(self.terse_output[TERSE_READ_IOPS_POSITION])

    def get_write_iops(self):
        return int(self.terse_output[TERSE_WRITE_IOPS_POSITION])

    def get_total_write_io(self):
        return int(self.terse_output[TERSE_TOTAL_IO_WRITE_POSITION])

    def get_write_latency(self):
        return [float(self.terse_output[TERSE_WRITE_LATENCY_START_POSITION]),  # min
                float(self.terse_output[TERSE_WRITE_LATENCY_START_POSITION + 1]),  # max
                float(self.terse_output[TERSE_WRITE_LATENCY_START_POSITION + 2])]  # mean

    def get_read_latency(self):
        return [float(self.terse_output[TERSE_READ_LATENCY_START_POSITION]),
                float(self.terse_output[TERSE_READ_LATENCY_START_POSITION + 1]),
                float(self.terse_output[TERSE_READ_LATENCY_START_POSITION + 2])]

    def get_read_throughput(self):
        return int(self.terse_output[TERSE_TOTAL_READ_THROUGHPUT_POSITION])

    def get_write_throughput(self):
        return int(self.terse_output[TERSE_TOTAL_WRITE_THROUGHPUT_POSITION])

    @classmethod
    def fio_path_and_version(cls, fio_path):
        fio_version = None
        if fio_path is None:
            fio = subprocess.Popen(['which', 'fio'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout = fio.communicate()[0]
            if fio.returncode != 0:
                logging.error("Error: command 'which fio' returned an error code.")
                raise RuntimeError("'which fio' returned an error.")
            fio_path = stdout.rsplit("\n")
        elif not is_exe(fio_path):
            logging.error("Error: cannot find {0} or {0} is not an executable.".format(fio_path))
            raise RuntimeError("Cannot find {0} or {0} is not an executable.".format(fio_path))

        fio = subprocess.Popen([fio_path, "--version"], stdout=subprocess.PIPE)
        fio_version = fio.communicate()[0]

        return fio_path, fio_version
