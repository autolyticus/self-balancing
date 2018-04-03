#!/usr/bin/env python3

from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET,
                    SO_REUSEADDR, SO_BROADCAST)
from time import sleep

# Set up UDP Socket for broadcasting self IP
BDestIP = '255.255.255.255'
BDestPort = 12321
BDest = (BDestIP, BDestPort)

usock = socket(AF_INET, SOCK_DGRAM)
usock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
usock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while True:
    usock.sendto('GG'.encode(), BDest)
    sleep(5)

