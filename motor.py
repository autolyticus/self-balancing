#!/usr/bin/env python3

import pigpio
import time

from phy import phytogpio


class DCMotor:
    def __init__(self, pi=None, enable=0, cw=0, ccw=0):
        self.pi = pi
        self.physenable, self.physcw, self.physccw = enable, cw, ccw
        self.enable, self.cw, self.ccw = (phytogpio[enable],
                                          phytogpio[cw], phytogpio[ccw])
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


class StepperMotor:
    def __init__(self, pi=None, enable=0, pins=(0, 0, 0, 0)):
        self.pi = pi
        self.enable = phytogpio[enable]
        (self.pin1, self.pin2,
         self.pin3, self.pin4) = (phytogpio[pins[0]], phytogpio[pins[1]],
                                  phytogpio[pins[2]], phytogpio[pins[3]])

        self.pi.set_mode(self.enable, pigpio.OUTPUT)
        self.pi.set_mode(self.pin1, pigpio.OUTPUT)
        self.pi.set_mode(self.pin2, pigpio.OUTPUT)
        self.pi.set_mode(self.pin3, pigpio.OUTPUT)
        self.pi.set_mode(self.pin4, pigpio.OUTPUT)
        self.pi.write(self.enable, 1)
        self.conv360 = 540

    def stepForward(self, delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

    def stepBackward(self, delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)

    def setStep(self, v1, v2, v3, v4):
        self.pi.write(self.pin1, v1)
        self.pi.write(self.pin2, v2)
        self.pi.write(self.pin3, v3)
        self.pi.write(self.pin4, v4)

    def angleMovement(self, angle, timeDiff):
        numSteps = self.conv360 / 360 * angle
        if angle > 0:
            self.stepForward(timeDiff, numSteps)
        elif angle < 0:
            numSteps = -1 * numSteps
            self.stepBackward(timeDiff, numSteps)
        else:
            self.stop()

    def stop(self):
        self.setStep(0, 0, 0, 0)


def Motor(type, **kwargs):
    if type == 'stepper':
        return StepperMotor(**kwargs)
    elif type == 'dc':
        return DCMotor(**kwargs)
