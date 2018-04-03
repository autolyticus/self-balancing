#!/usr/bin/env python3

import subprocess
import time

try:
    subprocess.call('./MPU/mpud &> /dev/null &', shell=True)
    time.sleep(1)

except:
    print("MPUD doesn't seem to be compiled???")
    exit()

try:
    if subprocess.call('pgrep -a pigpiod &> /dev/null', shell=True):
        subprocess.call('sudo pigpiod', shell=True)
    subprocess.call('python3 ./broadcaster.py &', shell=True)
    subprocess.call('python3 ./botcontrol.py &', shell=True)
    subprocess.call('python3 ./pid.py', shell=True)
    while True:
        pass

except:
    subprocess.call('pkill mpud', shell=True)
    subprocess.call('pkill -f "broadcaster.py"', shell=True)
    subprocess.call('pkill -f "botcontrol.py"', shell=True)
    subprocess.call('pkill -f "pid.py"', shell=True)

finally:
    subprocess.call('pkill mpud', shell=True)
    subprocess.call('pkill -f "broadcaster.py"', shell=True)
    subprocess.call('pkill -f "botcontrol.py"', shell=True)
    subprocess.call('pkill -f "pid.py"', shell=True)
