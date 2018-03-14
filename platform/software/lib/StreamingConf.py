# -*- coding: utf-8 -*-

import yaml
import os


class StreamingConf:

    def __init__(self, conf_file):
        home_dir = os.environ['MYSTR_HOME']
        f = open(home_dir + '/conf/' + conf_file, 'r')
        self.conf = yaml.load(f)
        f.close()
    
    #def get_job_manager(self):
    #    return self.conf['job_manager']
    
    def get_jm_address(self):
        return self.conf['job_manager']['address']

    def get_jm_mac(self):
        return self.conf['job_manager']['mac']

    def get_jm_port(self):
        return self.conf['job_manager']['port']

    def get_task_managers(self):
        return self.conf['task_manager']

    def get_tm_address(self, name):
        return self.conf['task_manager'][name]['address']

    def get_tm_mac(self, name):
        return self.conf['task_manager'][name]['mac']

    def get_tm_port(self, name):
        return self.conf['task_manager'][name]['port']

    def get_tm_device_type(self, name):
        return self.conf['task_manager'][name]['device_type']

    def get_tm_slots(self, name):
        return self.conf['task_manager'][name]['slots']

    def get_tm_data_interfaces(self, name):
        interfaces = self.conf['task_manager'][name]['data_interfaces']
        return tuple(interfaces)

    def get_network_bundling(self):
        return self.conf['network_event_bundling']
