# -*- coding: utf-8 -*-

from BaseOperator import BaseOperator
import yaml
import os


class BaseFPGAOperator(BaseOperator):

    def __init__(self, name):
        super().__init__(name)

