# -*- coding: utf-8 -*-

import struct

from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator
from JobInterface import JobInterface
from BaseJob import BaseJob

class Master(OperatorInterface, BaseOperator):

    def prepare(self):
        self.file_name = '/tmp/sha256.out'
        f = open(self.file_name, 'w')
        f.close()
        self.calculating = False
        self.i = 0


    def run(self):
        if self.calculating:
            if not self.in_streams[0].empty():
                nonce = struct.unpack('<I', self.in_streams[0].get())[0]
                f = open(self.file_name, 'a')
                f.write(str(nonce) + '\n')
                f.close()
                self.calculating = False
        else:
            if not self.out_streams[0].full():
                header = struct.pack('<QQQQQQQQQQQQQQQQ',\
                                     self.i,\
                                     0x1111111111111111,\
                                     0x2222222222222222,\
                                     0x3333333333333333,\
                                     0x4444444444444444,\
                                     0x5555555555555555,\
                                     0x6666666666666666,\
                                     0x7777777777777777,\
                                     0x8888888888888888,\
                                     0x200000ff00000000,\
                                     0x8000000000000000,\
                                     0x0000000000000000,\
                                     0x0000000000000000,\
                                     0x0000000000000000,\
                                     0x0000000000000000,\
                                     0x0000000000000280)
                                     #0x0102030405060708,\
                                     #0x1112131415161718,\
                                     #0x2122232425262728,\
                                     #0x3132333435363738,\
                                     #0x4142434445464748,\
                                     #0x5152535455565758,\
                                     #0x6162636465666768,\
                                     #0x7172737475767778,\
                                     #0x8182838485868788,\
                                     #0x200fffff00000000,\
                                     #0x9192939495969798,\
                                     #0xa1a2a3a4a5a6a7a8,\
                                     #0xb1b2b3b4b5b6b7b8,\
                                     #0xc1c2c3c4c5c6c7c8,\
                                     #0xd1d2d3d4d5d6d7d8,\
                                     #0xe1e2e3e4e5e6e7e8)
                self.out_streams[0].put(header)
                self.i += 1
                self.calculating = True

    def pause(self):
        pass

    def cancel(self):
        pass


class Worker(OperatorInterface, BaseOperator):

    def prepare(self):
        pass

    def run(self):
        pass

    def pause(self):
        pass

    def cancel(self):
        pass


class UserJob(JobInterface, BaseJob):

    def define_dataflow(self):

        master = Master('master')
        worker = Worker('worker')

        self.df.add_node(master)
        self.df.add_node(worker)

        self.df.add_edge(master, 0, worker, 0)
        self.df.add_edge(worker, 0, master, 0)

        th1 = self.create_thread_local_group(master)
        th2 = self.create_thread_local_group(worker)

        self.create_device_local_group('sv0', 'CPU', th1)
        self.create_device_local_group('fpga0', 'FPGA', th2)

