# -*- coding: utf-8 -*-

from StreamingConf import StreamingConf
from JobManagerInfo import JobManagerInfo
from TaskManagerInfo import TaskManagerInfo
from ResourceManagerInfo import ResourceManagerInfo


class ClusterInfo:

    def __init__(self):
        conf = StreamingConf('cluster.yaml')
        task_managers = conf.get_task_managers()
        self.task_manager_infos = {}
        for name in task_managers:
            manager_addr = conf.get_tm_address(name)
            manager_mac = conf.get_tm_mac(name)
            manager_port = conf.get_tm_port(name)
            device_type = conf.get_tm_device_type(name)
            if device_type == 'CPU':
                slots = conf.get_tm_slots(name)
            elif device_type == 'FPGA':
                slots = None
            else:
                slots = None
            data_interfaces = tuple(conf.get_tm_data_interfaces(name))
            info = TaskManagerInfo(name, manager_mac, manager_addr, manager_port, device_type, slots, data_interfaces)
            self.task_manager_infos[name] = info
        jm_mac = conf.get_jm_mac()
        jm_ip = conf.get_jm_address()
        jm_port = conf.get_jm_port()
        self.job_manager_info = JobManagerInfo(jm_mac, jm_ip, jm_port)
        rm_ip = conf.get_rm_address()
        rm_port = conf.get_rm_port()
        self.resource_manager_info = ResourceManagerInfo(rm_ip, rm_port)
