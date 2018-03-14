# -*- coding: utf-8 -*-

from WindowingTestOperators import *
from JobInterface import JobInterface
from BaseJob import BaseJob


class UserJob(JobInterface, BaseJob):

    def define_dataflow(self):

        generator0 = EventGenerator('gen0')
        generator1 = EventGenerator('gen1')
        generator2 = EventGenerator('gen2')
        generator3 = EventGenerator('gen3')
        generator4 = EventGenerator('gen4')
        generator5 = EventGenerator('gen5')
        generator6 = EventGenerator('gen6')
        generator7 = EventGenerator('gen7')
        aggregator = Aggregator('agg')
        windowing = HardwareWindowing('windowing', 'windowing.conf')
        receiver  = ResultReceiver('recv')

        self.df.add_node(generator0)
        self.df.add_node(generator1)
        self.df.add_node(generator2)
        self.df.add_node(generator3)
        self.df.add_node(generator4)
        self.df.add_node(generator5)
        self.df.add_node(generator6)
        self.df.add_node(generator7)
        self.df.add_node(aggregator)
        self.df.add_node(windowing)
        self.df.add_node(receiver)

        self.df.add_edge(generator0, 0, aggregator, 0)
        self.df.add_edge(generator1, 0, aggregator, 1)
        self.df.add_edge(generator2, 0, aggregator, 2)
        self.df.add_edge(generator3, 0, aggregator, 3)
        self.df.add_edge(generator4, 0, aggregator, 4)
        self.df.add_edge(generator5, 0, aggregator, 5)
        self.df.add_edge(generator6, 0, aggregator, 6)
        self.df.add_edge(generator7, 0, aggregator, 7)
        self.df.add_edge(aggregator, 0, windowing,  0)
        self.df.add_edge(windowing,  0, receiver,   0)

        gen_th0 = self.create_thread_local_group(generator0)
        gen_th1 = self.create_thread_local_group(generator1)
        gen_th2 = self.create_thread_local_group(generator2)
        gen_th3 = self.create_thread_local_group(generator3)
        gen_th4 = self.create_thread_local_group(generator4)
        gen_th5 = self.create_thread_local_group(generator5)
        gen_th6 = self.create_thread_local_group(generator6)
        gen_th7 = self.create_thread_local_group(generator7)
        agg_th  = self.create_thread_local_group(aggregator)
        win_th  = self.create_thread_local_group(windowing)
        rec_th  = self.create_thread_local_group(receiver)

        self.create_device_local_group('sv0', 'CPU', gen_th0, gen_th1, gen_th2, gen_th3,gen_th4,\
                                                     gen_th5, gen_th6, gen_th7, agg_th, rec_th)
        self.create_device_local_group('fpga0', 'FPGA', win_th)
