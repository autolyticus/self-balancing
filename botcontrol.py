#!/usr/bin/env python3

import pigpio
import time
from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET,
                    SO_REUSEADDR)

from motor import Motor
import threading


thisPi = pigpio.pi()

# And here's the actual TCP Socket for getting bot control commands
sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

sock.bind(('0.0.0.0', 32123))

m1 = Motor(pi=thisPi, type='stepper', pins=(37, 36, 38, 40))
m2 = Motor(pi=thisPi, type='stepper', pins=(35, 33, 31, 32))


def botMoveForward():
    print("Forward")
    m1.rotate(255)
    m2.rotate(255)


def botMoveBackward():
    print('Backward')
    m1.rotate(-255)
    m2.rotate(-255)


def botTurnLeft():
    print('Left')
    m1.rotate(255)
    m2.rotate(-255)


def botTurnRight():
    print('Right')
    m1.rotate(-255)
    m2.rotate(255)


def botStop():
    print('Stop')
    m1.rotate(0)
    # m2.rotate(0)


def performAction(data):
    if data == 'w':
        botMoveForward()
    elif data == 's':
        botMoveBackward()
    elif data == 'a':
        botTurnLeft()
    elif data == 'd':
        botTurnRight()
    elif data == 'z':
        botStop()


# client, addr = sock.accept()
# import pdb; pdb.set_trace()
# print(f'Connection established from {client.getpeername()}')

action = ''


class controlThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def run(self):
        global action
        while True:
            while action != '.':
                performAction(action)
                time.sleep(self.delay)
            while action == '.':
                pass
        action=''

    def __init__(self):
        super(controlThread, self).__init__()
        self._stop_event = threading.Event()

        # Reduce this value until controlling doesn't interfere with PID
        self.delay = 0.1

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


cThread = controlThread()
cThread.start()

try:
    while True:
        data = sock.recv(1)
        action = data.decode()
        # time.sleep(10)
except:
    pass

finally:
    # m1.rotate(0)
    # m2.rotate(0)
    pass
