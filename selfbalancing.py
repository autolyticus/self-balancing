#!/usr/bin/env python3

import pigpio
# import time

# from phy import phytogpio
from motor import Motor

from pidcontroller import PIDController

try:
    shm = open('/dev/shm/MPU', 'r')
except:
    print("MPUD doesn't seem to be started???")
    exit()

thisPi = pigpio.pi()
m1 = Motor(pi=thisPi, type='stepper', pins=(37, 36, 38, 40))

# When MPUD is running, reads the values from SHM location


def getMPUVals():
    global shm
    shm.seek(0, 0)
    output = shm.readline()
    a, b, c = output.split()
    return float(a), float(b), float(c)


# m1 = motor(pi, 22, 13, 15)
# m2 = motor(pi, 24, 18, 16)
m1.rotate(0)
# m2.rotate(0)


def botMoveForward(power):
    m1.rotate(power)
    # m2.rotate(power)


def botMoveBackward(power):
    # power = power * 1.5
    m1.rotate(power)
    # m2.rotate(power)


def botEquilibrium():
    m1.rotate(0)
    # m2.rotate(0)


PID = PIDController(P=50, I=0.01, D=1)
#import pdb; pdb.set_trace()
try:
    while True:
        a, b, c = getMPUVals()
        print(f'{a} {b} {c}')
        PIDx = PID.step(b)
        print(PIDx)
        if PIDx < 0.0:
            botMoveBackward(PIDx)
        elif PIDx > 0.0:
            botMoveForward(PIDx)
        else:
            botEquilibrium()

        # m1.rotate(255)
        # m2.rotate(255)
        # time.sleep(0.001)
except:
    pass

finally:
    m1.rotate(0)
    m2.rotate(0)
    pass
