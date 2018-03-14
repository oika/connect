# -*- coding: utf-8 -*-

from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator
from JobInterface import JobInterface
from BaseJob import BaseJob
import time


class Generator(OperatorInterface, BaseOperator):

    def __init__(self, name, *args):
        super().__init__(name, *args)
        self.checkpoint = args[0]
        self.logname = args[1]

    def prepare(self):
        self.count = 0
        f = open('/tmp/' + self.logname, 'w')
        f.close()
        self.old = 0
        self.now = 0

    def run(self):
        if not self.out_streams[0].full():
            self.out_streams[0].put(self.count)
            self.count += 1
            if self.count == self.checkpoint:
                self.count = 0 
                self.old = self.now
                self.now = time.time()
                if self.old != 0:
                    f = open('/tmp/' + self.logname, 'a')
                    f.write(str(self.now) + '\t' + str(self.checkpoint / (self.now - self.old)) + '\n')
                    f.close()

    def cancel(self):
        pass


class Receiver(OperatorInterface, BaseOperator):

    def __init__(self, name, *args):
        super().__init__(name, *args)
        self.checkpoint = args[0]
        self.logname = args[1]

    def prepare(self):
        self.count = 0
        f = open('/tmp/' + self.logname, 'w')
        f.close()
        self.old = 0
        self.now = 0

    def run(self):
        if not self.in_streams[0].empty():
            event = self.in_streams[0].get()
            self.count += 1
            if self.count == self.checkpoint:
                self.count = 0
                self.old = self.now
                self.now = time.time()
                if self.old != 0:
                    f = open('/tmp/' + self.logname, 'a')
                    f.write(str(self.now) + '\t' + str(self.checkpoint / (self.now - self.old)) + '\n')
                    f.close()

    def cancel(self):
        pass


class UserJob(JobInterface, BaseJob):

    def define_dataflow(self):

        checkpoint = 50000

        # create operators
        gen0 = Generator('gen0', checkpoint, 'gen0_speed')
        gen1 = Generator('gen1', checkpoint, 'gen1_speed')
        recv = Receiver('recv', checkpoint, 'recv_speed')

        # add operators to data-flow graph
        self.df.add_node(gen0)
        self.df.add_node(gen1)
        self.df.add_node(recv)

        # add edges
        self.df.add_edge(gen0, 0, recv, 0)
        self.df.add_edge(gen1, 0, recv, 0)

        # specify threads
        th_gen0 = self.create_thread_local_group(gen0)
        th_gen1 = self.create_thread_local_group(gen1)
        th_recv = self.create_thread_local_group(recv)

        # spcify devices
        self.create_device_local_group('sv0', 'CPU', th_gen0, th_gen1)
        self.create_device_local_group('sv1', 'CPU', th_recv)
