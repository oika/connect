# -*- coding: utf-8 -*-

from WindowingTestOperators import *
from JobInterface import JobInterface
from BaseJob import BaseJob


class UserJob(JobInterface, BaseJob):

    def define_dataflow(self):

        generator = EventGenerator('gen')
        windowing = HardwareWindowing('windowing', 'windowing.conf')
        receiver  = ResultReceiver('recv')

        self.df.add_node(generator)
        self.df.add_node(windowing)
        self.df.add_node(receiver)

        self.df.add_edge(generator, 0, windowing, 0)
        self.df.add_edge(windowing, 0, receiver, 0)

        th1 = self.create_thread_local_group(generator)
        th2 = self.create_thread_local_group(windowing)
        th3 = self.create_thread_local_group(receiver)

        #self.create_device_local_group('sv0', 'CPU', th1)
        self.create_device_local_group('sv0', 'CPU', th1, th3)
        self.create_device_local_group('fpga0', 'FPGA', th2)
