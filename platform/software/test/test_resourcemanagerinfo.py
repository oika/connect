# -*- coding: utf-8 -*-

from ResourceManagerInfo import ResourceManagerInfo

import unittest

class TestResourceManagerInfo(unittest.TestCase):

    def test_get_properties(self):
        info = ResourceManagerInfo("192.168.1.2", 1234)
        self.assertEqual(info.manager_address, "192.168.1.2")
        self.assertEqual(info.manager_port, 1234)

    def test_cannot_set_ip_addr(self):
        with self.assertRaises(AttributeError):
            info = ResourceManagerInfo("127.0.0.1", 12345)
            info.manager_address = "192.168.1.1"

    def test_cannot_set_port(self):
        with self.assertRaises(AttributeError):
            info = ResourceManagerInfo("127.0.0.1", 12345)
            info.manager_port = 222
    
if __name__=='__main__':
    unittest.main()
