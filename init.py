#!/usr/bin/env python3

import subprocess as s
from shlex import split
import time

processes = []

try:
    if s.call('pgrep -a imud &> /dev/null', shell=True):
        print('Starting imud')
        s.call('./imud/imud &> /dev/null &', shell=True)
    if s.call('pgrep -a pigpiod &> /dev/null', shell=True):
        print('Starting pigpiod')
        try:
            a = s.Popen(split('pigpiod'), shell=True)
        except FileNotFoundError:
            print('Please install pigpio library')
    time.sleep(1)

except FileNotFoundError:
    print('MPUD doesnt seem to be compiled')
    exit()

try:
            # processes.append(
            #     s.Popen(split('python3 ./broadcaster.py &'), shell=True))
            # processes.append(
            #     s.Popen(split('python3 ./botcontrol.py &'), shell=True))
    processes.append(s.call('python3 ./selfbalancing.py', shell=True))
    while True:
        pass

except:
    for process in processes:
        process.terminate()
    # s.call('pkill mpud', shell=True)
    # s.call('pkill -f "broadcaster.py"', shell=True)
    # s.call('pkill -f "botcontrol.py"', shell=True)
    # s.call('pkill -f "pid.py"', shell=True)

finally:
    for process in processes:
        process.terminate()
    # s.call('pkill mpud', shell=True)
    # s.call('pkill -f "broadcaster.py"', shell=True)
    # s.call('pkill -f "botcontrol.py"', shell=True)
    # s.call('pkill -f "pid.py"', shell=True)
