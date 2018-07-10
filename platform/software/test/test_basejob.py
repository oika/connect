# -*- coding: utf-8 -*-

import unittest
from BaseJob import BaseJob
from Dataflow import Dataflow
from ThreadLocalGroup import ThreadLocalGroup
from DeviceLocalGroup import DeviceLocalGroup
from OperatorInterface import OperatorInterface
from BaseOperator import BaseOperator

class MockOperator(OperatorInterface, BaseOperator):
    def prepare(self):
        pass

    def run(self):
        pass

    def cancel(self):
        pass
    
    def pause(self):
        pass

class TestBaseJob(unittest.TestCase):

    def test_init(self):
        job = BaseJob("foo")
        self.assertEqual(job.name, "foo")
        self.assertIsInstance(job.df, Dataflow)
        self.assertEqual(len(job.device_local_groups), 0)

    def test_device_local_groups(self):
        job = BaseJob("foo")
        job.create_device_local_group("g1", "CPU")
        job.create_device_local_group("g2", "CPU", ThreadLocalGroup(), ThreadLocalGroup())
        job.create_device_local_group("g1", "FPGA")  #same name
        res_dlgs = list(job.device_local_groups)
        self.assertEqual(len(res_dlgs), 2)
        self.assertEqual(res_dlgs[0].tm_name, "g1")
        self.assertEqual(res_dlgs[1].tm_name, "g2")
    
    def test_get_device_local_group(self):
        job = BaseJob("foo")
        job.create_device_local_group("g1", "CPU")
        job.create_device_local_group("g2", "CPU", ThreadLocalGroup(), ThreadLocalGroup())
        job.create_device_local_group("g1", "FPGA", ThreadLocalGroup(MockOperator("a"), MockOperator("b")))  #same name

        res1 = job.get_device_local_group("g1")
        self.assertEqual(res1.tm_name, "g1")
        self.assertEqual(res1.device_type, "FPGA")
        self.assertEqual(len(res1.tlgs), 1)
        self.assertEqual(len(res1.tlgs[0].operators), 2)
        self.assertEqual(res1.tlgs[0].operators[0].name, "a")
        self.assertIsInstance(res1.tlgs[0].operators[0], MockOperator)

        res2 = job.get_device_local_group("g2")
        self.assertEqual(res2.tm_name, "g2")
        self.assertEqual(res2.device_type, "CPU")
        self.assertEqual(len(res2.tlgs), 2)

        with self.assertRaises(KeyError):
            res3 = job.get_device_local_group("g3")
    

if __name__=='__main__':
    unittest.main()
