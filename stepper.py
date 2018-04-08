#!/usr/bin/python
# -*- coding: utf-8 -*-

import pigpio

from phy import phytogpio


class stepper:

    pi = None
    enable = 0
    physenable = 0
    physcw = 0
    physccw = 0
    pin1 = 0
    pin2 = 0
    pin3 = 0
    pin4 = 0
    conv360 = 540  # need to find proper value

    def __init__(self, pi, enable, pin1, pin2, pin3, pin4):
        self.pi = pi
        (self.physenable, self.physcw, self.physccw) = (enable, cw, ccw)
        self.enable = phytogpio[enable]
        (self.pin1, self.pin2, self.pin3, self.pin4) = \
            (phytogpio[pin1], phytogpio[pin2], phytogpio[pin3],
             phytogpio[pin4])
        self.pi.set_mode(self.enable, pigpio.OUTPUT)
        self.pi.set_mode(self.pin1, pigpio.OUTPUT)
        self.pi.set_mode(self.pin2, pigpio.OUTPUT)
        self.pi.set_mode(self.pin3, pigpio.OUTPUT)
        self.pi.set_mode(self.pin4, pigpio.OUTPUT)
        self.pi.write(self.enable, 1)

        def stepForward(self, delay, steps):
            for i in range(0, steps):
                setStep(1, 0, 0, 1)
                time.sleep(delay)
                setStep(0, 1, 1, 0)
                time.sleep(delay)
                setStep(0, 1, 0, 1)
                time.sleep(delay)
                setStep(1, 0, 0, 1)
                time.sleep(delay)

        def stepBackward(self, delay, steps):
            for i in range(0, steps):
                setStep(1, 0, 0, 1)
                time.sleep(delay)
                setStep(0, 1, 0, 1)
                time.sleep(delay)
                setStep(0, 1, 1, 0)
                time.sleep(delay)
                setStep(1, 0, 1, 0)
                time.sleep(delay)

        def setStep(v1, v2, v3, v4):
            self.pi.write(self.pin1, v1)
            self.pi.write(self.pin2, v2)
            self.pi.write(self.pin3, v3)
            self.pi.write(self.pin4, v4)

        def angleMovement(self, angle, timeDiff):
            numSteps = conv360 / 360 * angle
            if angle > 0:
                self.stepForward(timeDiff, numSteps)
            else:
                numSteps = -1 * numSteps
                self.stepBackward(timeDiff, numSteps)

    def stop(self):
        self.setStep(0, 0, 0, 0)