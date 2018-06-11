# -*- coding: utf-8 -*-

from queue import Empty
from Stream import *
import unittest


class TestNetworkStream(unittest.TestCase):

    def setUp(self):
        self.data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.event = 100
        self.address = '127.0.0.1'
        self.port = 5441
        self.rx = RxNetworkStream(self.address, self.port)
        self.tx = TxNetworkStream()
        self.tx.add_dest(self.address, self.port)

    def tearDown(self):
        del self.rx
        del self.tx

    def test_empty(self):
        assert not self.rx.empty()

    def test_full(self):
        assert not self.tx.full()

    def test_full_false(self):
        if not self.tx.full():
            self.tx.put(self.event.to_bytes(4, 'little'))
        if not self.rx.empty():
            self.rx.get()
        assert not self.tx.full()

    def test_put_get(self):
        for event in self.data:
            self.tx.put(event.to_bytes(4, 'little'))
            ret = int.from_bytes(self.rx.get(), 'little')
            assert ret == event

class TestMultipleNetworkStreams(unittest.TestCase):

    def setUp(self):
        self.event = 100
        self.address = '127.0.0.1'
        self.port_rx0 = 5441
        self.port_rx1 = 5442
        self.data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.rx0 = RxNetworkStream(self.address, self.port_rx0)
        self.rx1 = RxNetworkStream(self.address, self.port_rx1)
        self.tx0 = TxNetworkStream()
        self.tx1 = TxNetworkStream()

    def tearDown(self):
        del self.data
        del self.rx0
        del self.rx1
        del self.tx0
        del self.tx1

    def test_multi_tx_single_rx(self):
        self.tx0.add_dest(self.address, self.port_rx0)
        self.tx1.add_dest(self.address, self.port_rx0)

        while self.data:
            self.tx0.put(self.data[0].to_bytes(4, 'little'))
            event = int.from_bytes(self.rx0.get(), 'little')
            self.data.pop(self.data.index(event))
            self.tx1.put(self.data[0].to_bytes(4, 'little'))
            event = int.from_bytes(self.rx0.get(), 'little')
            self.data.pop(self.data.index(event))

        assert len(self.data) == 0

    def test_single_tx_multi_rx(self):
        self.tx0.add_dest(self.address, self.port_rx0)
        self.tx0.add_dest(self.address, self.port_rx1)

        while self.data:
            self.tx0.put(self.data[0].to_bytes(4, 'little'))
            event = int.from_bytes(self.rx0.get(), 'little')
            self.data.pop(self.data.index(event))
            self.tx0.put(self.data[0].to_bytes(4, 'little'))
            event = int.from_bytes(self.rx1.get(), 'little')
            self.data.pop(self.data.index(event))

        assert len(self.data) == 0

if __name__=='__main__':
    unittest.main()
