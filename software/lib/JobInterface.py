# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class JobInterface(metaclass=ABCMeta):
  @abstractmethod
  def define_dataflow(self):
    pass

