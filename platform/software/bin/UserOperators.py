# -*- coding: utf-8 -*-

from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator

class OperatorA(OperatorInterface, BaseOperator):

  def prepare(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/A.dat', 'w')
    f.close()

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/A.dat', 'a')
    f.write('x\n')
    f.close()
    if not self.out_stream['A-B'].full():
      self.out_stream['A-B'].put(1)

  def cancel(self):
    pass


class OperatorB(OperatorInterface, BaseOperator):

  def prepare(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/B.dat', 'w')
    f.close()
    pass

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/B.dat', 'a')
    f.write('x\n')
    f.close()
    if not self.out_stream['B-G'].full():
      if not self.in_stream['A-B'].empty():
        val = self.in_stream['A-B'].get()
        val += 1
        self.out_stream['B-G'].put(val)

  def cancel(self):
    pass


class OperatorC(OperatorInterface, BaseOperator):

  def prepare(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/C.dat', 'w')
    f.close()
    pass

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/C.dat', 'a')
    f.write('x\n')
    f.close()
    if not self.out_stream['C-D'].full():
      self.out_stream['C-D'].put(10)

  def cancel(self):
    pass


class OperatorD(OperatorInterface, BaseOperator):

  def prepare(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/D.dat', 'w')
    f.close()
    pass

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/D.dat', 'a')
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
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/E.dat', 'w')
    f.close()
    pass

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/E.dat', 'a')
    f.write('x\n')
    f.close()
    if not self.out_stream['E-F'].full():
      self.out_stream['E-F'].put(100)

  def cancel(self):
    pass


class OperatorF(OperatorInterface, BaseOperator):

  def prepare(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/F.dat', 'w')
    f.close()
    pass

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/F.dat', 'a')
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
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/G.dat', 'w')
    f.close()
    self.count = 0
    self.in_stream_list = list(self.in_stream.values())

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/G.dat', 'a')
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
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/H.dat', 'w')
    f.close()
    pass

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/H.dat', 'a')
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
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/I.dat', 'w')
    f.close()
    pass

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/I.dat', 'a')
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
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/J.dat', 'w')
    f.close()
    self.count = 0
    self.in_stream_list = list(self.in_stream.values())

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/J.dat', 'a')
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
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/K.dat', 'w')
    f.close()
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/output.dat', 'w')
    f.close()

  def run(self):
    f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/K.dat', 'a')
    f.write('x\n')
    f.close()
    if not self.in_stream['J-K'].empty():
      val = self.in_stream['J-K'].get()
      f = open('/home/efukuda/Repositories/github/ericfukuda/MyStreaming/tmp/output.dat', 'a')
      f.write(str(val) + '\n')
      f.close()

  def cancel(self):
    pass

class Operator1(OperatorInterface, BaseOperator):

  def prepare(self):
    self.f = open('/home/efukuda/Projects/MyStreaming/tmp/1.dat', 'w')

  def run(self):
    if not self.out_stream['1-2'].full():
      self.f.write('x\n')
      self.out_stream['1-2'].put(1)

  def cancel(self):
    self.f.close()


class Operator2(OperatorInterface, BaseOperator):

  def prepare(self):
    output_file = '/home/efukuda/Projects/MyStreaming/tmp/2.dat'
    self.f = open(output_file, 'w')

  def run(self):
    if not self.in_stream['1-2'].empty():
      val = self.in_stream['1-2'].get()
      val += 1
      self.f.write(str(val) + '\n')

  def cancel(self):
    self.f.close()

