# -*- coding: utf-8 -*-

import random
import time
import uuid
import struct
#from Job import *
#from Operator import *
from JobInterface import JobInterface
from BaseJob import BaseJob
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
        self.ad_num = 100
        self.event_type_idx = 0
        self.event_type_len = len(self.event_types)

    def run(self):
        if not self.out_streams[0].full():
            data = (self.user_id,\
                    self.page_id,\
                    random.randrange(self.ad_num),
                    #uuid.UUID(int=(self.ad_template.int + random.randrange(self.ad_num))),\
                    self.banner_id,\
                    self.event_types[self.event_type_idx],\
                    int(time.time()),\
                    self.user_addr)

            if self.event_type_idx == self.event_type_len - 1:
                self.event_type_idx = 0
            else:
                self.event_type_idx += 1

            if data[4] == 'view':
                message = struct.pack('<I', data[5]) + struct.pack('<I', data[2])
                self.out_streams[0].put(message, True)
                print(message)
                print('\n')
                #self.output.put((data[2], data[5]))

    def cancel(self):
        pass


class ResultReceiver(OperatorInterface, BaseOperator):
    def prepare(self):
        pass

    def run(self):
        if not self.in_streams[0].empty():
            counts = self.input.get()
            print(counts)

    def cancel(self):
        pass

class HardwareWindowing(BaseFPGAOperator):
    pass

#class FPGAOperator(OperatorInterface, BaseOperator):
#    def prepare(self):
#        self.window_size = 10 # in seconds
#        self.windows = {}
#        self.checkpoint_time = 0
#        self.ad_num = 100
#        self.campaign_num = 10
#        self.redis = redis.Redis('localhost', 6379)
#        template_file = '/home/efukuda/Repositories/github/ericfukuda/MyStreaming/bin/uuid_template'
#        with open(template_file, 'r') as f:
#            uuid_string = f.read().strip('\n')
#            self.ad_template = uuid.UUID(uuid_string)
#        self.campaign_template = uuid.UUID(int=(uuid.uuid4().int & 0xFFFFFFFFFFFFFFFFFFFFFFFF00000000))
#        self.ad_campaign_map = {}
#        campaign_cnt = 0
#        for ad_cnt in range(self.ad_num):
#            ad_uuid = uuid.UUID(int=(self.ad_template.int + ad_cnt))
#            campaign_uuid = uuid.UUID(int=(self.campaign_template.int + (ad_cnt % self.campaign_num)))
#            self.ad_campaign_map[ad_uuid] = campaign_uuid
#        self.input = self.instream[0]
#
#    def run(self):
#        if not self.input.empty():
#            event = self.input.get()
#            val = event[0]
#            event_time_float = event[1]
#            event_time = int(event_time_float)
#            campaign = self.ad_campaign_map[val]
#            window_time = event_time - event_time % self.window_size
#            if self.checkpoint_time == 0:
#                self.checkpoint_time = event_time
#            if self.windows.get(window_time) is None:
#                self.windows[window_time] = {campaign: 1}
#            elif self.windows[window_time].get(campaign) is None:
#                self.windows[window_time][campaign] = 1
#            else:
#                self.windows[window_time][campaign] += 1
#
#            if event_time >= self.checkpoint_time + 1:
#                write_event_time = (event_time - 1) - (event_time - 1) % self.window_size
#                self.windows[write_event_time]['last_update'] = event_time_float
#                self.redis.set(write_event_time, str(self.windows[write_event_time]))
#                self.checkpoint_time = event_time
#
#    def cancel(self):
#        pass

class UserJob(JobInterface, BaseJob):

    def define_dataflow(self):

        generator = EventGenerator('gen')
        windowing = HardwareWindowing('windowing', 'windowing.conf')
        receiver  = ResultReceiver('recv')


        self.df.add_node(generator)
        self.df.add_node(windowing)
        self.df.add_node(receiver)

        self.df.add_edge(generator, 0, windowing, 0)
        self.df.add_edge(windowing, 0, receiver, 0)

        th1 = self.create_thread_local_group(generator)
        th2 = self.create_thread_local_group(windowing)
        th3 = self.create_thread_local_group(receiver)

        self.create_device_local_group('sv0', 'CPU', th1, th3)
        self.create_device_local_group('fpga0', 'FPGA', th2)
