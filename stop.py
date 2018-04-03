#!/usr/bin/env python3

import pigpio
from motor import motor

pi = pigpio.pi()
m1 = motor(pi, 22, 13, 15)
m2 = motor(pi, 24, 18, 16)
m1.rotate(0)
m2.rotate(0)
try:
    import pdb; pdb.set_trace()
finally:
    m1.rotate(0)
    m2.rotate(0)
