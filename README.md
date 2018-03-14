# self-balancing
Self-Balancing Platform Implementation in a Pi - 3

Requires PiGPIO library and Python Bindings. All code is in Python 3.

Instructions: Go to MPU folder and run
```sh
$ make
$ ./mpud > /dev/null &
```

mpud is a simple daemon that uses the readings from the Digital Media Processor (DMP) of the IMU (MPU-6050) and stores the latest values in the SHM location /dev/shm/MPU. Thus, to get the latest readings (x, y, z angles) all that is needed to read the contents of this memory location as a file.

Now, class motor has a simple motor implementation for PWM control of a DC motor. Note that the power parameter is in the range 0-255.
Here's an example usage of the motor class:
```python
m1 = motor(enable = 22, cw = 13, ccw = 15)
m1.rotate(255) # Full power forwards
m2.rotate(-255) # Half power backwards
```

### Note: All pin numbers are Physical Pin numbers.

