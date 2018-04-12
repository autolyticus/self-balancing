#!/usr/bin/env python3

import pigpio
import time
import subprocess as s

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
        # self.pi = pi
        # self.enable = phytogpio[enable]
        # (self.pin0, self.pin1,
        #  self.pin2, self.pin3) = (phytogpio[pins[0]], phytogpio[pins[1]],
        #                           phytogpio[pins[2]], phytogpio[pins[3]])
        # self.pi.set_mode(self.pin0, pigpio.OUTPUT)
        # self.pi.set_mode(self.pin1, pigpio.OUTPUT)
        # self.pi.set_mode(self.pin2, pigpio.OUTPUT)
        # self.pi.set_mode(self.pin3, pigpio.OUTPUT)

        # if enable != 0:
        #     self.pi.set_mode(self.enable, pigpio.OUTPUT)
        #     self.pi.write(self.enable, 1)

        # self.stepAngle = 1.8
        # self.smallDelay = 0.0007
        # self.currentStep = 0
        # self.stopped = False
        self.motorProcess = s.Popen(
            ['./stepd/stepd.c.out', *[str(pin) for pin in pins]], stdin=s.PIPE)

    def rotate(self, power):
        power = int(power)
        self.motorProcess.stdin.write((str(power) + '\n').encode())
        self.motorProcess.stdin.flush()

    # def setStep(self, nextStep):
    #     self.pi.write(self.pin0, StepperMotor.stepSignal[nextStep][0])
    #     self.pi.write(self.pin1, StepperMotor.stepSignal[nextStep][1])
    #     self.pi.write(self.pin2, StepperMotor.stepSignal[nextStep][2])
    #     self.pi.write(self.pin3, StepperMotor.stepSignal[nextStep][3])
    #     self.currentStep = nextStep

    # def stepForward(self, steps=1, delay=0):
    #     if delay == 0:
    #         delay = self.smallDelay
    #     for i in range(steps):
    #         self.setStep((self.currentStep+1) % len(StepperMotor.stepSignal))
    #         time.sleep(delay)

    # def stepBackward(self, steps=1, delay=0):
    #     if delay == 0:
    #         delay = self.smallDelay
    #     for i in range(steps):
    #         self.setStep((self.currentStep-1) % len(StepperMotor.stepSignal))
    #         time.sleep(delay)

    # def angleMovement(self, angle=0, delay=0):
    #     numSteps = int(angle / (self.stepAngle))
    #     if angle > 0:
    #         self.stepForward(steps=numSteps, delay=delay)
    #     elif angle < 0:
    #         self.stepBackward(steps=-numSteps, delay=delay)
    #     else:
    #         self.stop()

    def stop(self):
        self.rotate(0)
        # for pin in [self.pin0, self.pin1, self.pin2, self.pin3]:
        #     self.pi.write(pin, 0)

    def release(self):
        self.rotate(0)
        self.motorProcess.terminate()


def Motor(**kwargs):
    if kwargs.get('type') == 'stepper':
        kwargs.pop('type', None)
        return StepperMotor(**kwargs)
    elif kwargs.get('type') == 'dc':
        kwargs.pop('type', None)
        return DCMotor(**kwargs)


if __name__ == '__main__':
    pass
