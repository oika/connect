# -*- coding: utf-8 -*-

import struct
import time
import uuid
import random
from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator
from BaseFPGAOperator import BaseFPGAOperator
from JobInterface import JobInterface
from BaseJob import BaseJob


class EventGenerator(OperatorInterface, BaseOperator):

    def prepare(self):
        self.n_bundle = 1
        self.c_bundle = 0
        self.c_event = 0
        self.checkpoint = 0
        self.pack = 32
        self.ad_num = 1000000
        self.performance_log = str(uuid.uuid4()) + '.log'
        self.data = b''
        for i in range(self.pack):
            self.data += struct.pack('<Q', i)
        with open(self.performance_log, 'w'):
            pass


    def run(self):
        self.c_event += 1
        if self.c_bundle == 0:
            self.message = self.data
        else:
            self.message += self.data

        if self.c_bundle == self.n_bundle - 1:
            self.c_bundle = 0
            self.out_streams[0].put(self.message)
            if self.c_event > self.checkpoint:
                with open(self.performance_log, 'a') as f:
                    f.write('{}\t{}\n'.format(time.time(), self.c_event))
                    self.checkpoint += 1000000
                self.data = b''
                for i in range(self.pack):
                    self.data += struct.pack('<I', int(time.time()))\
                                 + struct.pack('<I', random.randrange(self.ad_num))
        else:
            self.c_bundle += 1
        time.sleep(0.1)


    def pause(self):
        pass


    def cancel(self):
        pass


class HardwareWindowing(BaseFPGAOperator):
    pass


class UserJob(JobInterface, BaseJob):

    def define_dataflow(self):

        generator0 = EventGenerator('gen0')
        generator1 = EventGenerator('gen1')
        generator2 = EventGenerator('gen2')
        generator3 = EventGenerator('gen3')
        generator4 = EventGenerator('gen4')
        generator5 = EventGenerator('gen5')
        generator6 = EventGenerator('gen6')
        generator7 = EventGenerator('gen7')
        windowing = HardwareWindowing('windowing', 'windowing.conf')


        self.df.add_node(generator0)
        self.df.add_node(generator1)
        self.df.add_node(generator2)
        self.df.add_node(generator3)
        self.df.add_node(generator4)
        self.df.add_node(generator5)
        self.df.add_node(generator6)
        self.df.add_node(generator7)
        self.df.add_node(windowing)

        self.df.add_edge(generator0, 0, windowing, 0)
        self.df.add_edge(generator1, 0, windowing, 0)
        self.df.add_edge(generator2, 0, windowing, 0)
        self.df.add_edge(generator3, 0, windowing, 0)
        self.df.add_edge(generator4, 0, windowing, 0)
        self.df.add_edge(generator5, 0, windowing, 0)
        self.df.add_edge(generator6, 0, windowing, 0)
        self.df.add_edge(generator7, 0, windowing, 0)

        gen_th0 = self.create_thread_local_group(generator0)
        gen_th1 = self.create_thread_local_group(generator1)
        gen_th2 = self.create_thread_local_group(generator2)
        gen_th3 = self.create_thread_local_group(generator3)
        gen_th4 = self.create_thread_local_group(generator4)
        gen_th5 = self.create_thread_local_group(generator5)
        gen_th6 = self.create_thread_local_group(generator6)
        gen_th7 = self.create_thread_local_group(generator7)
        win_th  = self.create_thread_local_group(windowing)

        self.create_device_local_group('sv0', 'CPU', gen_th0, gen_th1, gen_th2, gen_th3,gen_th4,\
                                                     gen_th5, gen_th6, gen_th7)
        self.create_device_local_group('fpga0', 'FPGA', win_th)
