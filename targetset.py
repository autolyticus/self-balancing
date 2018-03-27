#!/usr/bin/env python3

import pigpio
import time

from phy import phytogpio

try:
    shm = open('/dev/shm/MPU', 'r')
except:
    print("MPUD doesn't seem to be started???")
    exit()

pi = pigpio.pi()

# When MPUD is running, reads the values from SHM location
def getMPUVals():
    global shm
    shm.seek(0, 0)
    output = shm.readline()
    a,b,c = output.split()
    return float(a),float(b),float(c)

sumb = 0
try:
    for i in range(1000):
        a,b,c = getMPUVals()
        sumb += b
    print(sumb/1000)

except:
    pass

finally:
    pass
