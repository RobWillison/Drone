import MotorDrive
from time import sleep

MotorDrive.setup()

mFrontLeft = MotorDrive.MOTOR1
mFrontRight = MotorDrive.MOTOR2
mBackLeft = MotorDrive.MOTOR3
mBackRight = MotorDrive.MOTOR4

def calibrate(motor):
    motor.setMotorValue(0)
    sleep(2)
    motor.setMotorValue(100)
    sleep(2)
    motor.setMotorValue(0)

calibrate(mFrontRight)
calibrate(mFrontLeft)
calibrate(mBackRight)
calibrate(mBackLeft)