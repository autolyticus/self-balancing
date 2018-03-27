#!/usr/bin/env python3

import pigpio
from motor import Motor

thisPi = pigpio.pi()
m1 = Motor(pi=thisPi, type='stepper', pins=(37, 36, 38, 40))
m1.stop()
import pdb; pdb.set_trace()
m1.angleMovement(360)
m1.angleMovement(-360)
