#!/usr/bin/env python3

import pigpio

from phy import phytogpio

class motor():
    enable = 0
    cw = 0
    ccw = 0
    physenable = 0
    physcw = 0
    physccw = 0

    def __init__(self, enable, cw, ccw):
        self.physenable, self.physcw, self.physccw = enable, cw, ccw
        self.enable, self.cw, self.ccw = phytogpio[enable], phytogpio[cw], phytogpio[ccw]
        pi.set_mode(self.enable, pigpio.OUTPUT)
        pi.set_mode(self.cw, pigpio.OUTPUT)
        pi.set_mode(self.ccw, pigpio.OUTPUT)
        pi.write(self.enable, 1)
        pi.write(self.cw, 0)
        pi.write(self.ccw, 0)

    def rotate(self, power):
        scale = 1
        power = scale * power
        if power == 0:
            pi.write(self.ccw, 0)
            pi.write(self.cw, 0)
        elif power > 0:
            pi.set_PWM_dutycycle(self.ccw, 0)
            pi.set_PWM_dutycycle(self.cw, int(power))
        else:
            pi.set_PWM_dutycycle(self.cw, 0)
            pi.set_PWM_dutycycle(self.ccw, int((-power)))
