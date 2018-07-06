# -*- coding: utf-8 -*-

from DataInterface import DataInterface

import unittest

class TestDataInterface(unittest.TestCase):

    def test_get_properties(self):
        data = DataInterface("00:00:00:00:00:00", "127.0.0.1", 12345)
        self.assertEqual(data.mac_addr, "00:00:00:00:00:00")
        self.assertEqual(data.ip_addr, "127.0.0.1")
        self.assertEqual(data.port, 12345)

    def test_cannot_set_mac_addr(self):
        with self.assertRaises(AttributeError):
            data = DataInterface("00:00:00:00:00:00", "127.0.0.1", 12345)
            data.mac_addr = "0a:0b:0c:0d:0e:0f"

    def test_cannot_set_ip_addr(self):
        with self.assertRaises(AttributeError):
            data = DataInterface("00:00:00:00:00:00", "127.0.0.1", 12345)
            data.ip_addr = "192.168.1.1"

    def test_cannot_set_port(self):
        with self.assertRaises(AttributeError):
            data = DataInterface("00:00:00:00:00:00", "127.0.0.1", 12345)
            data.port = 222
    
    def test_reserve(self):
        data = DataInterface("xx", "yy", 1)
        self.assertTrue(data.is_available)
        self.assertTrue(data.is_available)    # isn't changed by access.

        data.reserve()
        self.assertFalse(data.is_available)
        data.reserve()
        self.assertFalse(data.is_available)

        data.release()
        self.assertTrue(data.is_available)
        data.release()
        self.assertTrue(data.is_available)
        
        data.reserve()
        self.assertFalse(data.is_available)   # reserve again.
        
if __name__=='__main__':
    unittest.main()
