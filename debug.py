#!/usr/bin/env python3

import pigpio
from motor import Motor

thisPi = pigpio.pi()
m1 = Motor(pi=thisPi, type='stepper', pins=(37, 36, 38, 40))
m2 = Motor(pi=thisPi, type='stepper', pins=(35, 33, 31, 32))
import pdb; pdb.set_trace()
m1.release()
m2.release()
# m1.angleMovement(360)
# m1.angleMovement(-360)
