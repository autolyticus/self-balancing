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
m2 = Motor(pi=thisPi, type='stepper', pins=(35, 33, 31, 32))

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
m2.rotate(0)
# m2.rotate(0)


def botMoveForward(power):
    # power = power * 1.6
    m1.rotate(power)
    m2.rotate(power)


def botMoveBackward(power):
    power = power + 50
    # power = power * 1.6
    m1.rotate(power)
    m2.rotate(power)


def botEquilibrium():
    m1.rotate(0)
    m2.rotate(0)


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


with open('P', 'r') as f:
    kp = float(f.read())
with open('I', 'r') as f:
    ki = float(f.read())
with open('D', 'r') as f:
    kd = float(f.read())

PID = PIDController(P=kp, I=ki, D=kd)
# import pdb; pdb.set_trace()
try:
    while True:
        a, b, c = getMPUVals()
        b = b-1.5
        PIDx = PID.step(b)
        print(f'{b} {PIDx}')
        if PIDx < 0.0:
            #botMoveBackward(-map(-PIDx, 0, 1000, 40, 200))
            botMoveBackward(PIDx)
        elif PIDx > 0.0:
            #botMoveForward(map(PIDx, 0, 1000, 40, 200))
            botMoveForward(PIDx)
        else:
            botEquilibrium()

        # m1.rotate(255)
        # m2.rotate(255)
        # time.sleep(0.001)
except:
    pass

finally:
    # m1.rotate(0)
    # m2.rotate(0)
    m1.release()
    m2.release()
    pass
