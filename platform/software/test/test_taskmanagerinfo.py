# -*- coding: utf-8 -*-

from TaskManagerInfo import TaskManagerInfo

import unittest

class TestTaskManagerInfo(unittest.TestCase):

    def test_get_properties(self):
        info = TaskManagerInfo("foo", "xx:yy:zz", "192.168.1.2", 1234, "CPU", 2, [])
        self.assertEqual(info.name, "foo")
        self.assertEqual(info.manager_mac, "xx:yy:zz")
        self.assertEqual(info.manager_address, "192.168.1.2")
        self.assertEqual(info.manager_port, 1234)
        self.assertEqual(info.device_type, "CPU")
        self.assertEqual(info.slots, 2)
    
    def test_reserve_data_interface(self):
        ifs = [{"address":"a1", "mac":"m1", "port":1111}, {"address":"a2", "mac":"m2", "port":2222}]
        info = TaskManagerInfo("", "", "", 0, "", 0, ifs)

        resMc, resAd, resPt = info.reserve_data_interface()
        self.assertEqual(resMc, "m1")
        self.assertEqual(resAd, "a1")
        self.assertEqual(resPt, "1111")

        resMc, resAd, resPt = info.reserve_data_interface()
        self.assertEqual(resMc, "m2")
        self.assertEqual(resAd, "a2")
        self.assertEqual(resPt, "2222")

        n = info.reserve_data_interface()
        self.assertIsNone(n)

    
if __name__=='__main__':
    unittest.main()
