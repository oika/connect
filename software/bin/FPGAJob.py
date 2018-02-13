# -*- coding: utf-8 -*-

from JobInterface import JobInterface
from BaseJob import BaseJob
from FPGAOperators import *

class UserJob(JobInterface, BaseJob):

  def define_dataflow(self):

    sendOp = SendOperator('S')
    incrOp = IncrementOperator('I')
    recvOp = ReceiveOperator('R')

    self.df.add_node(sendOp)
    self.df.add_node(incrOp)
    self.df.add_node(recvOp)

    self.df.add_edge(sendOp, 0, incrOp, 0)
    self.df.add_edge(incrOp, 0, recvOp, 0)

    th1 = self.create_thread_local_group(sendOp)
    th2 = self.create_thread_local_group(incrOp)
    th3 = self.create_thread_local_group(recvOp)

    self.create_device_local_group('sv0', 'CPU', th1, th3)
    self.create_device_local_group('fpga0', 'FPGA', th2)

