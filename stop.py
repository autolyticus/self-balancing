#!/usr/bin/env python3

import pigpio
from motor import Motor

thisPi = pigpio.pi()
m1 = Motor(pi=thisPi, type='stepper', pins=(35, 36, 37, 38))
m2 = Motor(pi=thisPi, type='stepper', pins=(35, 33, 31, 32))
m1.release()
m2.release()
