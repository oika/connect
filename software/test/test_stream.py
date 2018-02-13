# -*- coding: utf-8 -*-

from Stream import *
from nose.tools import raises
from nose.tools import set_trace

class TestThreadLocalStream:

    @classmethod
    def setup_class(cls):
        cls.data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        cls.event = 100
        

    @classmethod
    def teardown_class(cls):
        pass


    def setup(self):
        self.stream = ThreadLocalStream()


    def teardown(self):
        del self.stream


    def test_init_empty(self):
        assert self.stream.empty()


    def test_init_full(self):
        assert not self.stream.full()


    @raises(Empty)
    def test_init_get(self):
        self.stream.get()


    def test_init_put(self):
        ret = self.stream.put(TestThreadLocalStream.event)
        assert ret == None


    def test_empty_true(self):
        self.stream.put(TestThreadLocalStream.event)
        self.stream.get()
        assert self.stream.empty()


    def test_empty_false(self):
        self.stream.put(TestThreadLocalStream.event)
        assert not self.stream.empty()


    def test_full_true(self):
        self.stream.put(TestThreadLocalStream.event)
        assert self.stream.full()


    def test_full_false(self):
        self.stream.put(TestThreadLocalStream.event)
        self.stream.get()
        assert not self.stream.full()


    def test_put_get(self):
        for event in TestThreadLocalStream.data:
            self.stream.put(event)
            ret = self.stream.get()
            assert ret == event


    @raises(Full)
    def test_multiple_put(self):
        for i in range(2):
            ret = self.stream.put(TestThreadLocalStream.event)


    @raises(Empty)
    def test_multiple_get(self):
        self.stream.put(TestThreadLocalStream.event)
        for i in range(2):
            ret = self.stream.get()


class TestInterThreadStream:

    @classmethod
    def setup_class(cls):
        cls.data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        cls.event = 100
        

    @classmethod
    def teardown_class(cls):
        pass


    def setup(self):
        self.stream = InterThreadStream()


    def teardown(self):
        del self.stream


    def test_init_empty(self):
        assert self.stream.empty()


    def test_init_full(self):
        assert not self.stream.full()


    @raises(Empty)
    def test_init_get(self):
        self.stream.get()


    def test_init_put(self):
        ret = self.stream.put(TestInterThreadStream.event)
        assert ret == None


    def test_empty_true(self):
        self.stream.put(TestInterThreadStream.event)
        self.stream.get()
        assert self.stream.empty()


    def test_empty_false(self):
        self.stream.put(TestInterThreadStream.event)
        assert not self.stream.empty()


    def test_full_true(self):
        self.stream.put(TestInterThreadStream.event)
        assert not self.stream.full()


    def test_full_false(self):
        self.stream.put(TestInterThreadStream.event)
        self.stream.get()
        assert not self.stream.full()


    def test_put_get(self):
        for event in TestInterThreadStream.data:
            self.stream.put(event)
            ret = self.stream.get()
            assert ret == event


    @raises(Empty)
    def test_multiple_get(self):
        self.stream.put(TestInterThreadStream.event)
        for i in range(2):
            ret = self.stream.get()


class TestNetworkStream:

    @classmethod
    def setup_class(cls):
        cls.data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        cls.event = 100
        cls.address = '127.0.0.1'
        cls.port = 5441
        

    @classmethod
    def teardown_class(cls):
        pass


    def setup(self):
        self.rx = RxNetworkStream(TestNetworkStream.address, TestNetworkStream.port)
        self.tx = TxNetworkStream()
        self.tx.add_dest(TestNetworkStream.address, TestNetworkStream.port)


    def teardown(self):
        del self.rx
        del self.tx


    def test_init_empty(self):
        assert self.rx.empty()


    def test_init_full(self):
        assert not self.tx.full()


    @raises(Empty)
    def test_init_get(self):
        self.rx.get()


    def test_init_put(self):
        ret = self.tx.put(TestNetworkStream.event)
        assert ret == None


    def test_empty_true(self):
        if not self.tx.full():
            self.tx.put(TestNetworkStream.event)
        if not self.rx.empty():
            self.rx.get()
        #set_trace()
        assert self.rx.empty()


    def test_empty_false(self):
        if not self.tx.full():
            self.tx.put(TestNetworkStream.event)
        assert not self.rx.empty()


    def test_full_true(self):
        self.tx.put(TestNetworkStream.event)
        assert not self.tx.full()


    def test_full_false(self):
        if not self.tx.full():
            self.tx.put(TestNetworkStream.event)
        if not self.rx.empty():
            self.rx.get()
        assert not self.tx.full()


    def test_put_get(self):
        for event in TestNetworkStream.data:
            if not self.tx.full():
                self.tx.put(event)
            if not self.rx.empty():
                ret = self.rx.get()
            assert ret == event


    @raises(Empty)
    def test_multiple_get(self):
        if not self.tx.full():
            self.tx.put(TestNetworkStream.event)
        if not self.rx.empty():
            for i in range(2):
                self.rx.get()


class TestMultipleNetworkStreams:

    @classmethod
    def setup_class(cls):
        cls.event = 100
        cls.address = '127.0.0.1'
        cls.port_rx0 = 5441
        cls.port_rx1 = 5442
        

    @classmethod
    def teardown_class(cls):
        pass


    def setup(self):
        self.data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.rx0 = RxNetworkStream(TestMultipleNetworkStreams.address, TestMultipleNetworkStreams.port_rx0)
        self.rx1 = RxNetworkStream(TestMultipleNetworkStreams.address, TestMultipleNetworkStreams.port_rx1)
        self.tx0 = TxNetworkStream()
        self.tx1 = TxNetworkStream()


    def teardown(self):
        del self.data
        del self.rx0
        del self.rx1
        del self.tx0
        del self.tx1


    def test_multi_tx_single_rx(self):
        self.tx0.add_dest(TestMultipleNetworkStreams.address, TestMultipleNetworkStreams.port_rx0)
        self.tx1.add_dest(TestMultipleNetworkStreams.address, TestMultipleNetworkStreams.port_rx0)

        for i in range(len(self.data)):
            if i%2 == 0 and not self.tx0.full():
                self.tx0.put(self.data[i])
            if i%2 == 1 and not self.tx1.full():
                self.tx1.put(self.data[i])

        while not self.rx0.empty():
            event = self.rx0.get()
            self.data.pop(self.data.index(event))

        assert len(self.data) == 0


    def test_single_tx_multi_rx(self):
        self.tx0.add_dest(TestMultipleNetworkStreams.address, TestMultipleNetworkStreams.port_rx0)
        self.tx0.add_dest(TestMultipleNetworkStreams.address, TestMultipleNetworkStreams.port_rx1)

        for i in range(len(self.data)):
            if not self.tx0.full():
                self.tx0.put(self.data[i])

        while not self.rx0.empty():
            event = self.rx0.get()
            self.data.pop(self.data.index(event))

        while not self.rx1.empty():
            event = self.rx1.get()
            self.data.pop(self.data.index(event))

        assert len(self.data) == 0
