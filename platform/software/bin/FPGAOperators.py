# -*- coding: utf-8 -*-

import os
import struct
from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator


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


class IncrementOperator(OperatorInterface, BaseOperator):

    def prepare(self):
        pass
    
    def run(self):
        #if not self.out_streams[0].full():
        #    if not self.in_streams[0].empty():
        event = self.in_streams[0].get()
        event += 1
        self.out_streams[0].put(event)
    
    def pause(self):
        pass
    
    def cancel(self):
        pass


class ReceiveOperator(OperatorInterface, BaseOperator):

    def prepare(self):
        self.file_name = '/tmp/fpga.out'
        f = open(self.file_name, 'w')
        f.close()
    
    def run(self):
        #if not self.in_streams[0].empty():
        event = struct.unpack('<Q', self.in_streams[0].get())
        f = open(self.file_name, 'a')
        f.write(str(event) + '\n')
        f.close()
    
    def pause(self):
        pass
    
    def cancel(self):
        pass
