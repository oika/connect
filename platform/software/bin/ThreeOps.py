# -*- coding: utf-8 -*-

from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator
from JobInterface import JobInterface
from BaseJob import BaseJob


class Operator1(OperatorInterface, BaseOperator):

    def prepare(self):
        self.f = open('/tmp/1.dat', 'w')

    def run(self):
        if not self.out_streams[0].full():
            self.out_streams[0].put(1)
            self.f.write(str(self.out_streams[0]) + '\n')

    def pause(self):
        pass

    def cancel(self):
        self.f.close()


class Operator2(OperatorInterface, BaseOperator):

    def prepare(self):
        self.f = open('/tmp/2.dat', 'w')

    def run(self):
        if not self.out_streams[0].full():
            self.out_streams[0].put(2)
            self.f.write(str(self.out_streams[0]) + '\n')

    def pause(self):
        pass

    def cancel(self):
        self.f.close()


class Operator3(OperatorInterface, BaseOperator):

    def prepare(self):
        self.f = open('/tmp/3.dat', 'w')

    def run(self):
        if not self.in_streams[0].empty():
            if not self.in_streams[1].empty():
                val1 = self.in_streams[0].get()
                val2 = self.in_streams[1].get()
                self.f.write(str(val1 + val2) + '\n')

    def pause(self):
        pass

    def cancel(self):
        self.f.close()
