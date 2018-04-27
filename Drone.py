import Adafruit_LSM9DS0
import MotorDrive
from time import sleep
import math
import PID
import redis

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

MotorDrive.setup()

mFrontLeft = MotorDrive.MOTOR1
mFrontRight = MotorDrive.MOTOR2
mBackLeft = MotorDrive.MOTOR3
mBackRight = MotorDrive.MOTOR4


def getMotorValue(motor):
    value = redisClient.get('motor-' + str(motor))
    if value == None:
        return 0
    return int(value)

while True:
    MotorDrive.setMotorValue(mFrontLeft, getMotorValue(1))
    MotorDrive.setMotorValue(mFrontRight, getMotorValue(2))
    MotorDrive.setMotorValue(mBackLeft, getMotorValue(3))
    MotorDrive.setMotorValue(mBackRight, getMotorValue(4))
    sleep(0.01)