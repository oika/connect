# -*- coding: utf-8 -*-

import queue
from abc import ABCMeta, abstractmethod


class BaseOperator:

    def __init__(self, name, *args):
        self.name = name
        self.args = args
        self.in_streams = {}
        self.out_streams = {}
