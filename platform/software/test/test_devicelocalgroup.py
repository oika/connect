# -*- coding: utf-8 -*-

import unittest
from DeviceLocalGroup import DeviceLocalGroup
from ThreadLocalGroup import ThreadLocalGroup
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

class TestDeviceLocalGroup(unittest.TestCase):

    def test_init(self):
        th1 = ThreadLocalGroup()
        th2 = ThreadLocalGroup()
        dlg = DeviceLocalGroup("name", "CPU", th1, th2)

        self.assertEqual(dlg.tm_name, "name")
        self.assertEqual(dlg.device_type, "CPU")
        self.assertListEqual(list(dlg.tlgs), [th1, th2])

    def test_tlgs_immutable(self):
        dlg = DeviceLocalGroup("name", "C", ThreadLocalGroup())
        with self.assertRaises(AttributeError):
            dlg.tlgs = (ThreadLocalGroup())
        
        with self.assertRaises(TypeError):
            dlg.tlgs[0] = ThreadLocalGroup()
    
    def test_has_operator(self):
        op1 = MockOperator("a")
        op2 = MockOperator("a")
        op3 = MockOperator("a")
        op4 = MockOperator("a")

        th1 = ThreadLocalGroup(op1)
        th2 = ThreadLocalGroup(op2, op3)
        dlg = DeviceLocalGroup("name", "C", th1, th2)
        self.assertTrue(dlg.has_operator(op1))
        self.assertTrue(dlg.has_operator(op2))
        self.assertTrue(dlg.has_operator(op3))
        self.assertFalse(dlg.has_operator(op4))

if __name__=='__main__':
    unittest.main()