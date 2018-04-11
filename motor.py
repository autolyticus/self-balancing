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
    stepSignal = ((1, 0, 1, 0), (0, 1, 1, 0), (0, 1, 0, 1), (1, 0, 0, 1))

    def __init__(self, pi=None, enable=0, pins=(0, 0, 0, 0)):
        self.pi = pi
        self.enable = phytogpio[enable]
        (self.pin1, self.pin2,
         self.pin3, self.pin4) = (phytogpio[pins[0]], phytogpio[pins[1]],
                                  phytogpio[pins[2]], phytogpio[pins[3]])
        self.pi.set_mode(self.pin1, pigpio.OUTPUT)
        self.pi.set_mode(self.pin2, pigpio.OUTPUT)
        self.pi.set_mode(self.pin3, pigpio.OUTPUT)
        self.pi.set_mode(self.pin4, pigpio.OUTPUT)

        if enable != 0:
            self.pi.set_mode(self.enable, pigpio.OUTPUT)
            self.pi.write(self.enable, 1)

        self.stepAngle = 1.8
        self.smallDelay = 0.006
        self.currentStep = 0

    def stepForward4(self, number, delay=0):
        if delay == 0:
            delay = self.smallDelay
        for i in range(0, number):
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

    def stepBackward4(self, delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)

    def setStep(self, stepSet):
        self.pi.write(self.pin1, StepperMotor.steps[stepSet])
        self.pi.write(self.pin2, StepperMotor.steps[stepSet])
        self.pi.write(self.pin3, StepperMotor.steps[stepSet])
        self.pi.write(self.pin4, StepperMotor.steps[stepSet])

    def angleMovement(self, angle, timeDiff):
        numSteps = int(angle / (self.stepAngle))
        if angle > 0:
            self.stepForward(timeDiff, numSteps)
        elif angle < 0:
            self.stepBackward(timeDiff, -numSteps)
        else:
            self.stop()

    def stop(self):
        self.pi.write(self.pin1, 0)
        self.pi.write(self.pin2, 0)
        self.pi.write(self.pin3, 0)
        self.pi.write(self.pin4, 0)


def Motor(**kwargs):
    if kwargs.get('type') == 'stepper':
        kwargs.pop('type', None)
        return StepperMotor(**kwargs)
    elif kwargs.get('type') == 'dc':
        kwargs.pop('type', None)
        return DCMotor(**kwargs)
