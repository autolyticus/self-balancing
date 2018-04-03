#!/usr/bin/env python3

import pigpio
import time

from phy import phytogpio
from motor import motor

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

m1 = motor(pi, 22, 13, 15)
m2 = motor(pi, 24, 18, 16)

try:
    while True:
        a,b,c = getMPUVals()
        print(f'{a} {b} {c}')
        m1.rotate(255)
        m2.rotate(255)
        time.sleep(0.01)
except:
    pass

finally:
    m1.rotate(0)
    m2.rotate(0)
    pass
