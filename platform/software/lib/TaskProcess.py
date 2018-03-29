#!/usr/bin/env python3
# -*- coding: utf-8

import multiprocessing


class TaskProcess(multiprocessing.Process):

    def __init__(self, tlg, ev_stop):
        super().__init__()
        self.tlg = tlg
        self.ev_stop = ev_stop

    def run(self):
        while True:
            if self.ev_stop.is_set():
                break
            for op in self.tlg.operators:
                op.run()
