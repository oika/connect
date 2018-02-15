# -*- coding: utf-8 -*-

from JobInterface import JobInterface
from BaseJob import BaseJob
from UserOperators import *

class UserJob(JobInterface, BaseJob):

  def define_dataflow(self):

    op1 = Operator1('1')
    op2 = Operator2('2')

    self.df.add_node(op1)
    self.df.add_node(op2)

    self.df.add_edge(op1, op2)

    th1 = self.create_thread_local_group(op1)
    th2 = self.create_thread_local_group(op2)

    self.create_device_local_group('cpu1', 'CPU', th1, th2)
    #self.create_device_local_group('1.1.1.2', 'CPU', th2)

