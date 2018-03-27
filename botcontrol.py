#!/usr/bin/env python3

import pigpio
import time
from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET,
                    SO_REUSEADDR)

from motor import Motor


thisPi = pigpio.pi()


# And here's the actual TCP Socket for getting bot control commands
sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

sock.bind(('0.0.0.0', 32123))
sock.listen(1)

m1 = Motor(pi=thisPi, pins=(35, 36, 37, 38))
# m2 = Motor(pi=thisPi, 24, 18, 16)


def botMoveForward():
    print("Forward")
    m1.rotate(255)
    # m2.rotate(255)


def botMoveBackward():
    print('Backward')
    m1.rotate(-255)
    # m2.rotate(-255)


def botTurnLeft():
    print('Left')
    m1.rotate(255)
    # m2.rotate(-255)


def botTurnRight():
    print('Right')
    m1.rotate(-255)
    # m2.rotate(255)


def botStop():
    print('Stop')
    m1.rotate(0)
    # m2.rotate(0)


def performAction(data):
    data = data.decode()
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


client, addr = sock.accept()
# import pdb; pdb.set_trace()
print(f'Connection established from {client.getpeername()}')

try:
    while True:
        data = client.recv(1)
        import pdb
        pdb.set_trace()
        performAction(data)
        # time.sleep(10)
except:
    pass

finally:
    # m1.rotate(0)
    # m2.rotate(0)
    pass
