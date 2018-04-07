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
	pin1=0
	pin2=0
	pin3=0
	pin4=0
	conv360 = 540	#need to find proper value

    def __init__(self, pi, enable, cw, ccw):
        self.pi = pi
        self.physenable, self.physcw, self.physccw = enable, cw, ccw
        self.enable, self.cw, self.ccw = phytogpio[enable], phytogpio[cw], phytogpio[ccw]
		self.pin1, self.pin2, self.pin3, self.pin4 = phytogpio[pin1], phytogpio[pin2], phytogpio[pin3], phytogpio[pin4]
        self.pi.set_mode(self.enable, pigpio.OUTPUT)
        self.pi.set_mode(self.cw, pigpio.OUTPUT)
        self.pi.set_mode(self.ccw, pigpio.OUTPUT)
		self.pi.set_mode(self.pin1, pigpio.OUTPUT)
		self.pi.set_mode(self.pin2, pigpio.OUTPUT)
		self.pi.set_mode(self.pin3, pigpio.OUTPUT)
		self.pi.set_mode(self.pin4, pigpio.OUTPUT)
        self.pi.write(self.enable, 1)
        self.pi.write(self.cw, 0)
        self.pi.write(self.ccw, 0)
		
	def stepForward( self, delay, steps ):
		for i in range(0, steps):
			setStep( 1, 0, 0, 1 )
			time.sleep( delay )
			setStep( 0, 1, 1, 0 )
			time.sleep( delay )
			setStep( 0, 1, 0, 1 )
			time.sleep( delay )
			setStep( 1, 0, 0, 1 )
			time.sleep( delay )
			
	def stepBackward( self, delay, steps ):
		for i in range (0, steps):
			setStep( 1, 0, 0, 1 )
			time.sleep( delay )
			setStep( 0, 1, 0, 1 )
			time.sleep( delay )
			setStep( 0, 1, 1, 0 )
			time.sleep( delay )
			setStep( 1, 0, 1, 0 )
			time.sleep( delay )
			
	def setStep( v1, v2, v3, v4 ):
		self.pi.write( self.pin1, v1 )
		self.pi.write( self.pin2, v2 )
		self.pi.write( self.pin3, v3 )
		self.pi.write( self.pin4, v4 )
		
	def angleMovement( self, angle, polarity, timeDiff ):	#polarity = +1 for forward, -1 for backward and timediff can be given from PID -> D/4...
		numSteps = conv360 / 360 * angle
		if polarity == 1:
			self.stepForward( timeDiff, numSteps )
		else:
			self.stepBackward( timeDiff, numSteps )

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