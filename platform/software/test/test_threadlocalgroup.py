# -*- coding: utf-8 -*-

import unittest
from ThreadLocalGroup import ThreadLocalGroup

class TestThreadLocalGroup(unittest.TestCase):
    def test_init(self):
        group = ThreadLocalGroup("t1", "t2", "t3")
        self.assertListEqual(list(group.operators), ["t1", "t2", "t3"])
    
    def test_operators_immutable(self):
        group = ThreadLocalGroup("t1", "t2", "t3")
        
        with self.assertRaises(AttributeError):
            group.operators = ["t4"]
        
        with self.assertRaises(TypeError):
            group.operators[0] = "t4"


if __name__=='__main__':
    unittest.main()