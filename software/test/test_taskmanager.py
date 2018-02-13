# -*- coding: utf-8 -*-

from TaskManager import TaskManager
from nose.tools import set_trace

class TestTaskManager:

    @classmethod
    def setup_class(cls):
        pass


    @classmethod
    def teardown_class(cls):
        pass


    def setup(self):
        self.tm = TaskManager('sv')


    def teardown(self):
        del self.tm


    def test_get_task_manager_info(self):
        pass


    def __attach_internal_stream(self, pre, suc, df):
        pass


    def __attach_internal_stream(self, pre, suc, df):
        pass


    def __attach_tx_stream(self, pre, suc, df, nw_if):
        pass


    def __attach_rx_stream(self, pre, suc, df, nw_if):
        pass


    def __attach_streams(self, df, dlg, nw_if):
        pass


    def prepare_tasks(self, job_name):
        pass


    def run_tasks(self, job_name):
        pass


    def pause_tasks(self, job_name):
        pass


    def cancel_tasks(self, job_name):
        pass
