# -*- coding: utf-8 -*-

from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator
from JobInterface import JobInterface
from BaseJob import BaseJob


class OperatorA(OperatorInterface, BaseOperator):

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
        op1  = OperatorA('1')
        op2  = OperatorA('2')

        self.df.add_node(op1)
        self.df.add_node(op2)

        self.df.add_edge(op1,  0, op2,  0)

        ps1 = self.create_thread_local_group(op1, op2)

        self.create_device_local_group('sv0', 'CPU', ps1)
