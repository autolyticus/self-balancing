#!/usr/bin/env python3

import subprocess as s
from shlex import split
import time

processes = []

try:
    processes.append(s.Popen(split('./imud/imud &> /dev/null &'), shell=True))
    time.sleep(1)

except FileNotFoundError:
    print('MPUD doesnt seem to be compiled')
    exit()

try:
    if s.call('pgrep -a pigpiod &> /dev/null', shell=True):
        print('Starting pigpiod')
        try:
            a = s.Popen(split('(sudo pigpiod) &'), shell=True)
        except FileNotFoundError:
            print('Please install pigpio library')

            # processes.append(
            #     s.Popen(split('python3 ./broadcaster.py &'), shell=True))
            # processes.append(
            #     s.Popen(split('python3 ./botcontrol.py &'), shell=True))
    processes.append(s.call('python3 ./selfbalancing.py', shell=True))
    while True:
        pass

except:
    pass
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
