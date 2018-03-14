#!/usr/bin/env python3
# -*- coding: utf-8

import multiprocessing


class TaskProcess(multiprocessing.Process):

    def __init__(self, tlg):
        super().__init__()
        self.tlg = tlg
        self.running = False
    
    def run(self):
        while self.running:
            for op in self.tlg.operators:
                op.run()
