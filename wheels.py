import motor
import stepper
from phy import phytogpio


class wheel:
    
    polarity = 0
    pi = None
    enable = 0
    cw = 0
    ccw = 0
    pin1 = 0
    pin2 = 0
    pin3 = 0
    pin4 = 0
    # wheeler if self cannot be used for this, wheeler may be used, i guess
    wheeler = 0

    def __init__(self, pi, enable, pin1, pin2, pin3, pin4):
        wheeler = stepper(pi, enable, pin1, pin2, pin3, pin4)
        polarity = 1

    def __init__(self, pi, enable, cw, ccw):
        wheeler = motor(pi, enable, cw, ccw)
        polarity = -1

    def move(self, power, timed):
        if polarity == -1:
            wheeler.rotate(power)
        else:
            wheeler.angleMovement(power, timed)

    def stop(self):
        wheeler.stop()
