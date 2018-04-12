#!/usr/bin/env python3

import pigpio
from motor import Motor

thisPi = pigpio.pi()
m1 = Motor(pi=thisPi, type='stepper', pins=(35, 36, 37, 38))
m1.stop()
