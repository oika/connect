# -*- coding: utf-8 -*-

from JobManagerInfo import JobManagerInfo

import unittest

class TestJobManagerInfo(unittest.TestCase):

    def test_get_properties(self):
        info = JobManagerInfo("00:00:00:00:00:00", "127.0.0.1", 12345)
        assert info.mac_addr is "00:00:00:00:00:00"
        assert info.ip_addr is "127.0.0.1"
        assert info.port is 12345

    def test_cannot_set_mac_addr(self):
        with self.assertRaises(AttributeError):
            info = JobManagerInfo("00:00:00:00:00:00", "127.0.0.1", 12345)
            info.mac_addr = "0a:0b:0c:0d:0e:0f"

    def test_cannot_set_ip_addr(self):
        with self.assertRaises(AttributeError):
            info = JobManagerInfo("00:00:00:00:00:00", "127.0.0.1", 12345)
            info.ip_addr = "192.168.1.1"

    def test_cannot_set_port(self):
        with self.assertRaises(AttributeError):
            info = JobManagerInfo("00:00:00:00:00:00", "127.0.0.1", 12345)
            info.port = 222
        
if __name__=='__main__':
    unittest.main()
