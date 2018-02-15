# -*- coding: utf-8 -*-

import random
import time
import uuid
import struct
import pickle
from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator
from BaseFPGAOperator import BaseFPGAOperator

class EventGenerator(OperatorInterface, BaseOperator):
    def prepare(self):
        self.user_id = uuid.uuid4()
        self.page_id = uuid.uuid4()
        with open('/home/efukuda/Projects/MyStreaming/bin/uuid_template', 'r') as f:
            uuid_string = f.read().strip('\n')
            self.ad_template = uuid.UUID(uuid_string)
        self.banner_id = 'banner78'
        self.event_types = ('view', 'click', 'purchase')
        self.user_addr = '1.2.3.4'
        self.ad_num = 1000000
        self.event_type_idx = 0
        self.event_type_len = len(self.event_types)
        self.event_counter = 0
        self.n_bundle = 128
        self.c_bundle = 0
        self.performance_log = str(uuid.uuid4()) + '.log'
        self.checkpoint = 1000000
        with open(self.performance_log, 'w'):
            pass

    def run(self):
        data = (self.user_id,\
                self.page_id,\
                random.randrange(self.ad_num),
                self.banner_id,\
                self.event_types[self.event_type_idx],\
                int(time.time()),\
                self.user_addr)
        self.event_counter += 1

        if self.event_type_idx == self.event_type_len - 1:
            self.event_type_idx = 0
        else:
            self.event_type_idx += 1

        if data[4] == 'view':
            if self.c_bundle == 0:
                self.message = struct.pack('<I', data[5]) + struct.pack('<I', data[2])
            else:
                self.message += struct.pack('<I', data[5]) + struct.pack('<I', data[2])

            if self.c_bundle == self.n_bundle - 1:
                self.c_bundle = 0
                self.out_streams[0].put(self.message)
                if self.event_counter > self.checkpoint:
                    with open(self.performance_log, 'a') as f:
                        f.write('{}\t{}\n'.format(time.time(), self.event_counter))
                        self.checkpoint += 1000000
            else:
                self.c_bundle += 1

    def pause(self):
        pass

    def cancel(self):
        pass


class ResultReceiver(OperatorInterface, BaseOperator):
    def prepare(self):
        pass

    def run(self):
        event = struct.unpack('<Q', self.in_streams[0].get())[0]
        timestamp = event & 0xffff
        campaign = (event & 0xfffff0000) >> 16
        count = (event & 0xfffffff000000000) >> 36
        print('time: {}, campaign: {}, count: {}'.format(timestamp, campaign, count))

    def pause(self):
        pass

    def cancel(self):
        pass


class HardwareWindowing(BaseFPGAOperator):
    pass

