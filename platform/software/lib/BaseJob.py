# -*- coding: utf-8 -*-

from Dataflow import Dataflow
from DeviceLocalGroup import DeviceLocalGroup
from ThreadLocalGroup import ThreadLocalGroup


class BaseJob:

    def __init__(self, name):
        self.name = name
        self.df = Dataflow()
        self.dlgs = {}

    def create_thread_local_group(self, *operators):
        tlg = ThreadLocalGroup(*operators)
        return tlg

    def create_device_local_group(self, tm_name, device_type, *thread_local_groups):
        dlg = DeviceLocalGroup(tm_name, device_type, *thread_local_groups)
        self.dlgs[dlg.tm_name] = dlg

    def get_device_local_group(self, tm_name):
        return self.dlgs[tm_name]
