#!/usr/bin/env python3

import pigpio
import time

from phy import phytogpio
from motor import motor


pi = pigpio.pi()

from socket import (socket, AF_INET, SOCK_STREAM, SOL_SOCKET,
                    SO_REUSEADDR)

# And here's the actual TCP Socket for getting bot control commands
sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

sock.bind(('0.0.0.0', 32123))
sock.listen(1)

m1 = motor(pi, 22, 13, 15)
m2 = motor(pi, 24, 18, 16)



def botMoveForward():
    m1.rotate(255)
    m2.rotate(255)

def botMoveBackward():
    m1.rotate(-255)
    m2.rotate(-255)

def botTurnLeft():
    m1.rotate(255)
    m2.rotate(-255)

def botTurnRight():
    m1.rotate(-255)
    m2.rotate(255)

def botStop():
    m1.rotate(0)
    m2.rotate(0)

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
#import pdb; pdb.set_trace()
print(f'Connection established from {client.getpeername()}')

try:
    while True:
        data = client.recv(1)
        import pdb; pdb.set_trace()
        performAction(data)
        #time.sleep(10)
except:
    pass

finally:
    # m1.rotate(0)
    # m2.rotate(0)
    pass
