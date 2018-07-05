# -*- coding: utf-8 -*-

import os
import struct
from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator
from BaseFPGAOperator import BaseFPGAOperator


class SendOperator(OperatorInterface, BaseOperator):

    def prepare(self):
        self.count = 0

    def run(self):
        #if not self.out_streams[0].full():
        message = struct.pack('<Q', self.count)
        self.out_streams[0].put(message)
        self.count += 2

    def pause(self):
        pass

    def cancel(self):
        pass

class IncrementOperator(BaseFPGAOperator):

    bitfile = 'design_1_wrapper.bit'

class ReceiveOperator(OperatorInterface, BaseOperator):

    def prepare(self):
        self.file_name = '/tmp/fpga.out'
        f = open(self.file_name, 'w')
        f.close()

    def run(self):
        print('here')
        event = struct.unpack('<Q', self.in_streams[0].get())
        f = open(self.file_name, 'a')
        f.write(str(event) + '\n')
        f.close()

    def pause(self):
        pass

    def cancel(self):
        pass
