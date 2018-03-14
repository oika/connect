# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class OperatorInterface(metaclass=ABCMeta):

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def cancel(self):
        pass
