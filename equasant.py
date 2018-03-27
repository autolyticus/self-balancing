#a python script to be used with Balancing robots

# Importing all necessary librarys and classes
from mpu6050 import mpu6050
from time import sleep
import math
from pidcontroller import PIDController
import  RPi.GPIO as GPIO

import pigpio
from motor import Motor 

thisPi = pigpio.pi()
m1 = Motor(pi=thisPi, type='stepper', pins=(37, 36, 38, 40))
m2 = Motor(pi=thisPi, type='stepper', pins=(35, 33, 31, 32))

#GPIO.setmode(GPIO.BCM) #Setting the Mode to use. I am using the BCM setup
#GPIO.setwarnings(False) 

##Declaring the GPIO Pins that the motor controller is set with
#int1 = 21
#int2 = 20
#int3 = 16
#int4 = 12

#GPIO.setup(int1, GPIO.OUT)
#GPIO.setup(int2, GPIO.OUT)
#GPIO.setup(int3, GPIO.OUT)
#GPIO.setup(int4, GPIO.OUT)

##Pulse width modulation: the speed changes accordingly the inclination angle
#PWM1 = GPIO.PWM(21, 100)
#PWM2 = GPIO.PWM(20, 100)
#PWM3 = GPIO.PWM(16, 100)
#PWM4 = GPIO.PWM(12, 100)


#PWM1.start(0)
#PWM2.start(0)
#PWM3.start(0)
#PWM4.start(0)
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

##This backward function takes a velocity argument that is the PID value. Both motors drives backward
def backward(velocity):
    velocity = -velocity
    vel = map(velocity, 0, 4000, 60, 200)
    vel = -vel
    m1.rotate(-vel)
    m2.rotate(-vel)
    # PWM1.ChangeDutyCycle(velocity)
    # GPIO.output(int2, GPIO.LOW)
    # PWM3.ChangeDutyCycle(velocity)
    # GPIO.output(int4, GPIO.LOW)

##Alike the backward funtion this forward function does the same thing but moves both the motors forward.
def forward(velocity):
    vel = map(velocity, 0, 4000, 60, 200)
    m1.rotate(vel)
    m2.rotate(vel)
    # GPIO.output(int1, GPIO.LOW)
    # PWM2.ChangeDutyCycle(velocity)
    # GPIO.output(int3, GPIO.LOW)
    # PWM4.ChangeDutyCycle(velocity)

##If the PID value is 0 (the Robot is 'balanced') it uses this equilibrium function.
def equilibrium():
    m1.rotate(0)
    m2.rotate(0)


sensor = mpu6050(0x68)
#K and K1 --> Constants used with the complementary filter
K = 0.98
K1 = 1 - K

time_diff = 0.02
ITerm = 0

#Calling the MPU6050 data 
accel_data = sensor.get_accel_data()
gyro_data = sensor.get_gyro_data()

aTempX = accel_data['x']
aTempY = accel_data['y']
aTempZ = accel_data['z']

gTempX = gyro_data['x']
gTempY = gyro_data['y']
gTempZ = gyro_data['z']

#some math 
def distance(a, b):
    return math.sqrt((a*a) + (b*b))

def y_rotation(x, y, z):
    radians = math.atan2(x, distance(y, z))
    return -math.degrees(radians)

def x_rotation(x, y, z):
    radians = math.atan2(y, distance(x, z))
    return math.degrees(radians)


last_x = x_rotation(aTempX, aTempY, aTempZ)
last_y = y_rotation(aTempX, aTempY, aTempZ)

gyro_offset_x = gTempX
gyro_offset_y = gTempY

gyro_total_x = (last_x) - gyro_offset_x
gyro_total_y = (last_y) - gyro_offset_y


#the so called 'main loop' that loops around and tells the motors wether to move or not 
while True:
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()

    accelX = accel_data['x']
    accelY = accel_data['y']
    accelZ = accel_data['z']

    gyroX = gyro_data['x']
    gyroY = gyro_data['y']
    gyroZ = gyro_data['z']

    gyroX -= gyro_offset_x
    gyroY -= gyro_offset_y

    gyro_x_delta = (gyroX * time_diff)
    gyro_y_delta = (gyroY * time_diff)

    gyro_total_x += gyro_x_delta
    gyro_total_y += gyro_y_delta

    rotation_x = x_rotation(accelX, accelY, accelZ)
    rotation_y = y_rotation(accelX, accelY, accelZ)
    
    #Complementary Filter
    # last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
    last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)
    # last_y = last_y - 15

    #setting the PID values. Here you can change the P, I and D values according to yiur needs
    PID = PIDController(P=50, I=0.0, D=0.0)
    # PIDx = PID.step(last_x)
    PIDy = PID.step(last_y)

    #if the PIDx data is lower than 0.0 than move appropriately backward
    if PIDy < 0.0:
        backward(float(PIDy))
        #StepperFor(-PIDx)
    #if the PIDx data is higher than 0.0 than move appropriately forward
    elif PIDy > 0.0:
        forward(float(PIDy))
        #StepperBACK(PIDx)
    #if none of the above statements is fulfilled than do not move at all 
    else:
        equilibrium()

    # print(last_x, 'PID: ', int(PIDx))
    print(last_y, 'PID: ', int(PIDy))
    #sleep(0.02)
