# -*- coding: utf-8 -*-

from Dataflow import Dataflow
from DeviceLocalGroup import DeviceLocalGroup
from ThreadLocalGroup import ThreadLocalGroup


class BaseJob:

    def __init__(self, name):
        self.__name = name
        self.__df = Dataflow()
        self.__dlgs = {}
    
    @property
    def name(self):
        return self.__name
    
    @property
    def df(self):
        return self.__df

    @property
    def device_local_groups(self):
        return self.__dlgs.values()

    def create_thread_local_group(self, *operators):
        tlg = ThreadLocalGroup(*operators)
        return tlg

    def create_device_local_group(self, tm_name, device_type, *thread_local_groups):
        dlg = DeviceLocalGroup(tm_name, device_type, *thread_local_groups)
        self.__dlgs[dlg.tm_name] = dlg

    def get_device_local_group(self, tm_name):
        return self.__dlgs[tm_name]
    

