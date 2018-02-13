# -*- coding: utf-8 -*-

from JobInterface import JobInterface
from BaseJob import BaseJob
from UserOperators import *

class UserJob(JobInterface, BaseJob):

  def define_dataflow(self):

    opA = OperatorA('A')
    opB = OperatorB('B')
    opC = OperatorC('C')
    opD = OperatorD('D')
    opE = OperatorE('E')
    opF = OperatorF('F')
    opG = OperatorG('G')
    opH = OperatorH('H')
    opI = OperatorI('I')
    opJ = OperatorJ('J')
    opK = OperatorK('K')

    self.df.add_node(opA)
    self.df.add_node(opB)
    self.df.add_node(opC)
    self.df.add_node(opD)
    self.df.add_node(opE)
    self.df.add_node(opF)
    self.df.add_node(opG)
    self.df.add_node(opH)
    self.df.add_node(opI)
    self.df.add_node(opJ)
    self.df.add_node(opK)
    self.df.add_edge(opA, opB)
    self.df.add_edge(opC, opD)
    self.df.add_edge(opE, opF)
    self.df.add_edge(opB, opG)
    self.df.add_edge(opD, opG)
    self.df.add_edge(opF, opG)
    self.df.add_edge(opG, opH)
    self.df.add_edge(opG, opI)
    self.df.add_edge(opH, opJ)
    self.df.add_edge(opI, opJ)
    self.df.add_edge(opJ, opK)

    th1 = self.create_thread_local_group(opA, opB)
    th2 = self.create_thread_local_group(opC, opD)
    th3 = self.create_thread_local_group(opE, opF)
    th4 = self.create_thread_local_group(opG, opH, opI, opJ)
    th5 = self.create_thread_local_group(opK)

    self.create_device_local_group('processor1', 'CPU', th1, th2, th3, th4, th5)

