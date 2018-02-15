# -*- coding: utf-8 -*-

from StreamingConf import StreamingConf
from JobManagerInfo import JobManagerInfo
from TaskManagerInfo import TaskManagerInfo

class ClusterInfo:

    def __init__(self):
        conf = StreamingConf('cluster.yaml')
        task_managers = conf.get_task_managers()
        self.task_manager_infos = {}
        for name in task_managers:
            manager_addr = conf.get_tm_address(name)
            manager_port = conf.get_tm_port(name)
            device_type = conf.get_tm_device_type(name)
            if device_type == 'CPU':
                slots = conf.get_tm_slots(name)
            elif device_type == 'FPGA':
                slots = None
            else:
                slots = None
            data_interfaces = tuple(conf.get_tm_data_interfaces(name))
            info = TaskManagerInfo(name, manager_addr, manager_port, device_type, slots, data_interfaces)
            self.task_manager_infos[name] = info
        job_manager = conf.get_job_manager()
        self.job_manager_info = JobManagerInfo(job_manager['address'], job_manager['port'])
