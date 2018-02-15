#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import glob
from os.path import basename

total = 0
event_size = float(sys.argv[1])
bundle_size = int(sys.argv[2])

for file in glob.glob('./*.log'):
    with open(file, 'r') as log:
        lines = log.readlines()
        first = lines[0]
        last = lines[-1]
        first_time  = float(first.split()[0])
        first_count = float(first.split()[1])
        last_time   = float(last.split()[0])
        last_count  = float(last.split()[1])
        perf = (last_count - first_count)/(last_time - first_time)
        total += perf

events = total * bundle_size
speed = event_size * events / 10**9
print('{:,} packets/s, {:,} events/s, {:.3f} Gbps'.format(int(total), int(events), speed))
