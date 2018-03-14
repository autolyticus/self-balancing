#!/usr/bin/env python3

import subprocess
import time

import pdb
# pdb.set_trace()
try:
    status = subprocess.call('./MPU/mpud &> /dev/null &', shell=True)
    time.sleep(1)
except:
    print("MPUD doesn't seem to be compiled???")
    exit()

try:
    import pid
except:
    pass
finally:
    status = subprocess.call('pkill mpud', shell=True)
    pass
