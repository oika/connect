# -*- coding: utf-8 -*-

from TaskManager import TaskManager
from multiprocessing import Process
from Stream import *
#import asyncore
import unittest
import multiprocessing


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.hostname = 'sv0'
        self.tm = TaskManager(self.hostname)
        self.tm.set_network()
        self.tm.addr = '127.0.0.1'
        self.tm.port = 5440
        self.job_name = 'tm_test'
        #self.tm.start_network()

    def tearDown(self):
        self.tm.close()
        del self.tm

    def __get_ops(self):
        tlgs = self.tm.jobs[self.job_name].dlgs[self.hostname].tlgs
        ops = {}
        for tlg in tlgs:
            for op in tlg.operators:
                ops[op.name] = op
        return ops

    def test_add_job_intra_process_single_edge(self):
        interfaces = {}
        self.tm.add_job('IntraProcessJob_SingleEdge.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].in_streams) == 1
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].in_streams[0], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['2'].in_streams[0]

    def test_add_job_intra_process_single_out(self):
        interfaces = {}
        self.tm.add_job('IntraProcessJob_SingleOut.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].in_streams) == 1
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].in_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[0], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['2'].in_streams[0]
        assert ops['1'].out_streams[0] is ops['3'].in_streams[0]
        assert ops['2'].in_streams[0] is ops['3'].in_streams[0]

    def test_add_job_intra_process_double_out(self):
        interfaces = {}
        self.tm.add_job('IntraProcessJob_DoubleOut.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 2
        assert len(ops['2'].in_streams) == 1
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['1'].out_streams[1], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].in_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[0], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops ['2'].in_streams[0]
        assert ops['1'].out_streams[1] is ops ['3'].in_streams[0]
        assert ops['2'].in_streams[0] is not ops['3'].in_streams[0]

    def test_add_job_intra_process_single_in(self):
        interfaces = {}
        self.tm.add_job('IntraProcessJob_SingleIn.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].out_streams) == 1
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[0], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['3'].in_streams[0]
        assert ops['2'].out_streams[0] is ops['3'].in_streams[0]
        assert ops['1'].out_streams[0] is ops['2'].out_streams[0]

    def test_add_job_intra_process_double_in(self):
        interfaces = {}
        self.tm.add_job('IntraProcessJob_DoubleIn.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].out_streams) == 1
        assert len(ops['3'].in_streams) == 2
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[1], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['3'].in_streams[0]
        assert ops['2'].out_streams[0] is ops['3'].in_streams[1]
        assert ops['1'].out_streams[0] is not ops['2'].out_streams[0]

    def test_add_job_inter_process_single_edge(self):
        interfaces = {}
        self.tm.add_job('InterProcessJob_SingleEdge.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].in_streams) == 1
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].in_streams[0], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['2'].in_streams[0]

    def test_add_job_inter_process_single_out(self):
        interfaces = {}
        self.tm.add_job('InterProcessJob_SingleOut.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].in_streams) == 1
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].in_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[0], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['2'].in_streams[0]
        assert ops['1'].out_streams[0] is ops['3'].in_streams[0]
        assert ops['2'].in_streams[0] is ops['3'].in_streams[0]

    def test_add_job_inter_process_double_out(self):
        interfaces = {}
        self.tm.add_job('InterProcessJob_DoubleOut.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 2
        assert len(ops['2'].in_streams) == 1
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['1'].out_streams[1], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].in_streams[0], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['2'].in_streams[0]
        assert ops['1'].out_streams[1] is ops['3'].in_streams[0]
        assert ops['2'].in_streams[0] is not ops['3'].in_streams[0]

    def test_add_job_inter_process_single_in(self):
        interfaces = {}
        self.tm.add_job('InterProcessJob_SingleIn.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].out_streams) == 1
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[0], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['3'].in_streams[0]
        assert ops['2'].out_streams[0] is ops['3'].in_streams[0]
        assert ops['1'].out_streams[0] is ops['2'].out_streams[0]

    def test_add_job_inter_process_double_in(self):
        interfaces = {}
        self.tm.add_job('InterProcessJob_DoubleIn.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].out_streams) == 1
        assert len(ops['3'].in_streams) == 2
        assert isinstance(ops['1'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['2'].out_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[0], multiprocessing.queues.Queue)
        assert isinstance(ops['3'].in_streams[1], multiprocessing.queues.Queue)
        assert ops['1'].out_streams[0] is ops['3'].in_streams[0]
        assert ops['2'].out_streams[0] is ops['3'].in_streams[1]
        assert ops['1'].out_streams[0] is not ops['2'].out_streams[0]

    def test_add_job_inter_device_single_edge_out(self):
        interfaces = {('2', 0):('127.0.0.1', 5441, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_SingleEdge_Out.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert isinstance(ops['1'].out_streams[0], TxNetworkStream)

    def test_add_job_inter_device_single_out_out(self):
        interfaces = {('2', 0):('127.0.0.1', 5441, '00:00:00:00:00:00'),
                      ('3', 0):('127.0.0.1', 5442, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_SingleOut_Out.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert isinstance(ops['1'].out_streams[0], TxNetworkStream)

    def test_add_job_inter_device_double_out_out(self):
        interfaces = {('2', 0):('127.0.0.1', 5441, '00:00:00:00:00:00'),
                      ('3', 0):('127.0.0.1', 5442, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_DoubleOut_Out.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 2
        assert isinstance(ops['1'].out_streams[0], TxNetworkStream)
        assert isinstance(ops['1'].out_streams[1], TxNetworkStream)
        assert ops['1'].out_streams[0] is not ops['1'].out_streams[1]

    def test_add_job_inter_device_single_in_out(self):
        interfaces = {('3', 0):('127.0.0.1', 5441, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_SingleIn_Out.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].out_streams) == 1
        assert isinstance(ops['1'].out_streams[0], TxNetworkStream)
        assert isinstance(ops['2'].out_streams[0], TxNetworkStream)
        assert ops['1'].out_streams[0] is not ops['2'].out_streams[0]

    def test_add_job_inter_device_double_in_out(self):
        interfaces = {('3', 0):('127.0.0.1', 5441, '00:00:00:00:00:00'),
                      ('3', 1):('127.0.0.1', 5442, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_DoubleIn_Out.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['1'].out_streams) == 1
        assert len(ops['2'].out_streams) == 1
        assert isinstance(ops['1'].out_streams[0], TxNetworkStream)
        assert isinstance(ops['2'].out_streams[0], TxNetworkStream)
        assert ops['1'].out_streams[0] is not ops['2'].out_streams[0]

    def test_add_job_inter_device_single_edge_in(self):
        interfaces = {('2', 0):('127.0.0.1', 5441, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_SingleEdge_In.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['2'].in_streams) == 1
        assert isinstance(ops['2'].in_streams[0], RxNetworkStream)
        del ops['2'].in_streams[0]

    def test_add_job_inter_device_single_out_in(self):
        interfaces = {('2', 0):('127.0.0.1', 5441, '00:00:00:00:00:00'),
                      ('3', 0):('127.0.0.1', 5442, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_SingleOut_In.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['2'].in_streams) == 1
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['2'].in_streams[0], RxNetworkStream)
        assert isinstance(ops['3'].in_streams[0], RxNetworkStream)
        assert ops['2'].in_streams[0] is not ops['3'].in_streams[0]
        del ops['2'].in_streams[0]

    def test_add_job_inter_device_double_out_in(self):
        interfaces = {('2', 0):('127.0.0.1', 5441, '00:00:00:00:00:00'),
                      ('3', 0):('127.0.0.1', 5442, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_DoubleOut_In.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['2'].in_streams) == 1
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['2'].in_streams[0], RxNetworkStream)
        assert isinstance(ops['3'].in_streams[0], RxNetworkStream)
        assert ops['2'].in_streams[0] is not ops['3'].in_streams[0]
        del ops['2'].in_streams[0]
        del ops['3'].in_streams[0]

    def test_add_job_inter_device_single_in_in(self):
        interfaces = {('3', 0):('127.0.0.1', 5441, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_SingleIn_In.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['3'].in_streams) == 1
        assert isinstance(ops['3'].in_streams[0], RxNetworkStream)
        del ops['3'].in_streams[0]

    def test_add_job_inter_device_double_in_in(self):
        interfaces = {('3', 0):('127.0.0.1', 5441, '00:00:00:00:00:00'),
                      ('3', 1):('127.0.0.1', 5442, '00:00:00:00:00:00')}
        self.tm.add_job('InterDeviceJob_DoubleIn_In.py', self.job_name, interfaces)
        ops = self.__get_ops()
        assert len(ops['3'].in_streams) == 2
        assert isinstance(ops['3'].in_streams[0], RxNetworkStream)
        assert isinstance(ops['3'].in_streams[1], RxNetworkStream)
        assert ops['3'].in_streams[0] is not ops['3'].in_streams[1]
        del ops['3'].in_streams[0]
        del ops['3'].in_streams[1]

    def test_prepare_tasks(self):
        pass

    def test_run_tasks(self):
        pass

    def test_pause_tasks(self):
        pass

    def test_cancel_tasks(self):
        pass

if __name__=='__main__':
    unittest.main()
