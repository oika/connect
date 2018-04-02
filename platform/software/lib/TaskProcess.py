#!/usr/bin/env python3
# -*- coding: utf-8

import multiprocessing


class TaskProcess(multiprocessing.Process):

    def __init__(self, tlg, running):
        super().__init__()
        self.tlg = tlg
        self.running = running

    def run(self):
        while True:
            self.running.wait()
            for op in self.tlg.operators:
                op.run()
