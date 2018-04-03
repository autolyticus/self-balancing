#!/usr/bin/env python3

import pigpio

from phy import phytogpio

class motor():
    pi = None
    enable = 0
    cw = 0
    ccw = 0
    physenable = 0
    physcw = 0
    physccw = 0

    def __init__(self, pi, enable, cw, ccw):
        self.pi = pi
        self.physenable, self.physcw, self.physccw = enable, cw, ccw
        self.enable, self.cw, self.ccw = phytogpio[enable], phytogpio[cw], phytogpio[ccw]
        self.pi.set_mode(self.enable, pigpio.OUTPUT)
        self.pi.set_mode(self.cw, pigpio.OUTPUT)
        self.pi.set_mode(self.ccw, pigpio.OUTPUT)
        self.pi.write(self.enable, 1)
        self.pi.write(self.cw, 0)
        self.pi.write(self.ccw, 0)

    def rotate(self, power):
        if power == 0:
            self.pi.write(self.ccw, 0)
            self.pi.write(self.cw, 0)
        elif power > 0:
            if power > 255:
                power = 255
            if power < 70:
                power = 70
            self.pi.set_PWM_dutycycle(self.ccw, 0)
            self.pi.set_PWM_dutycycle(self.cw, int(power))
        else:
            if power < -255:
                power = -255
            if power > -70:
                power = -70
            else:
                self.pi.set_PWM_dutycycle(self.cw, 0)
                self.pi.set_PWM_dutycycle(self.ccw, int((-power)))

    def stop(self):
        self.rotate(0)
