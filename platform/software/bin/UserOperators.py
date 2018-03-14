# -*- coding: utf-8 -*-

from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator


class OperatorA(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/a.dat', 'w')
        f.close()
    
    def run(self):
        f = open('/tmp/a.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_streams[0].full():
            self.out_streams[0].put(1)
    
    def cancel(self):
        pass


class OperatorB(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/b.dat', 'w')
        f.close()
        pass

    def run(self):
        f = open('/tmp/b.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_streams[0].full():
            if not self.in_streams[0].empty():
                val = self.in_streams[0].get()
                val += 1
                self.out_streams[0].put(val)

    def cancel(self):
        pass


class OperatorC(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/c.dat', 'w')
        f.close()
        pass

    def run(self):
        f = open('/tmp/c.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_stream['C-D'].full():
            self.out_stream['C-D'].put(10)

    def cancel(self):
        pass


class OperatorD(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/d.dat', 'w')
        f.close()
        pass

    def run(self):
        f = open('/tmp/d.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_stream['D-G'].full():
            if not self.in_stream['C-D'].empty():
                val = self.in_stream['C-D'].get()
                val += 1
                self.out_stream['D-G'].put(val)

    def cancel(self):
        pass


class OperatorE(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/e.dat', 'w')
        f.close()
        pass

    def run(self):
        f = open('/tmp/e.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_stream['E-F'].full():
            self.out_stream['E-F'].put(100)

    def cancel(self):
        pass


class OperatorF(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/f.dat', 'w')
        f.close()
        pass

    def run(self):
        f = open('/tmp/f.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_stream['F-G'].full():
            if not self.in_stream['E-F'].empty():
                val = self.in_stream['E-F'].get()
                val += 1
                self.out_stream['F-G'].put(val)

    def cancel(self):
        pass


class OperatorG(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/g.dat', 'w')
        f.close()
        self.count = 0
        self.in_stream_list = list(self.in_stream.values())

    def run(self):
        f = open('/tmp/g.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_stream['G-H'].full():
            if not self.out_stream['G-I'].full():
                while not self.in_stream_list[self.count%3].empty():
                    val = self.in_stream_list[self.count%3].get()
                    val += 2
                    if val > 100:
                        self.out_stream['G-H'].put(val)
                    else:
                        self.out_stream['G-I'].put(val)
                self.count += 1

    def cancel(self):
        pass


class OperatorH(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/h.dat', 'w')
        f.close()
        pass

    def run(self):
        f = open('/tmp/h.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_stream['H-J'].full():
            if not self.in_stream['G-H'].empty():
                val = self.in_stream['G-H'].get()
                val += 1
                self.out_stream['H-J'].put(val)

    def cancel(self):
        pass


class OperatorI(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/i.dat', 'w')
        f.close()
        pass
    
    def run(self):
        f = open('/tmp/i.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_stream['I-J'].full():
            if not self.in_stream['G-I'].empty():
                val = self.in_stream['G-I'].get()
                val += 1
                self.out_stream['I-J'].put(val)

    def cancel(self):
        pass


class OperatorJ(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/j.dat', 'w')
        f.close()
        self.count = 0
        self.in_stream_list = list(self.in_stream.values())

    def run(self):
        f = open('/tmp/j.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.out_stream['J-K'].full():
            while not self.in_stream_list[self.count%2].empty():
                val = self.in_stream_list[self.count%2].get()
                val += 1
                self.out_stream['J-K'].put(val)
            self.count += 1

    def cancel(self):
        pass


class OperatorK(OperatorInterface, BaseOperator):

    def prepare(self):
        f = open('/tmp/k.dat', 'w')
        f.close()
        f = open('/tmp/output.dat', 'w')
        f.close()

    def run(self):
        f = open('/tmp/k.dat', 'a')
        f.write('x\n')
        f.close()
        if not self.in_stream['J-K'].empty():
            val = self.in_stream['J-K'].get()
            f = open('/tmp/output.dat', 'a')
            f.write(str(val) + '\n')
            f.close()

    def cancel(self):
        pass

class Operator1(OperatorInterface, BaseOperator):

    def prepare(self):
        self.f = open('/tmp/1.dat', 'w')

    def run(self):
        if not self.out_streams[0].full():
            self.f.write('x\n')
            self.out_streams[0].put(1)

    def pause(self):
        pass

    def cancel(self):
        self.f.close()


class Operator2(OperatorInterface, BaseOperator):

    def prepare(self):
        output_file = '/tmp/2.dat'
        self.f = open(output_file, 'w')

    def run(self):
        if not self.in_streams[0].empty():
            val = self.in_streams[0].get()
            val += 1
            self.f.write(str(val) + '\n')

    def pause(self):
        pass

    def cancel(self):
        self.f.close()
