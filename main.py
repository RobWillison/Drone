import Adafruit_LSM9DS0
import MotorDrive
from time import sleep
import math

MotorDrive.setup()

mFrontLeft = MotorDrive.MOTOR1
mFrontRight = MotorDrive.MOTOR2
mBackLeft = MotorDrive.MOTOR3
mBackRight = MotorDrive.MOTOR4

imu = Adafruit_LSM9DS0.LSM9DS0()

fXg = 0
fYg = 0
fZg = 0
alpha = 0.5

def filterAccel():
  global fXg
  global fYg
  global fZg
  (Xg, Yg, Zg) = imu.readAccel()

  fXg = Xg * alpha + (fXg * (1 - alpha))
  fYg = Yg * alpha + (fYg * (1 - alpha))
  fZg = Zg * alpha + (fZg * (1 - alpha))

  return fXg, fYg, fZg

def pitch():
  Xg, Yg, Zg = filterAccel()

  pitch = math.atan2(Xg, math.sqrt(Yg**2 + Zg**2))
  global pitchCalibration
  return math.degrees(pitch) - pitchCalibration

def roll():
  Xg, Yg, Zg = filterAccel()

  roll = math.atan2(-Yg, Zg)
  global rollCalibration
  return math.degrees(roll) - rollCalibration


def getRollBias():
  rollAngle = roll()
  bias = (rollAngle / 180) + 0.5

  return bias

def getPitchBias():
  pitchAngle = pitch()
  bias = (pitchAngle / 180) + 0.5

  return bias

def setMotor(motor, value):
  if value >= 1:
      value = 1
  motor.value = value

totalPower = 0.1
rollCalibration = 0
pitchCalibration = 0
rollCalibration = roll()
pitchCalibration = pitch()

while(True):
  pitchBias = getPitchBias()
  rollBias = getRollBias()
  frontPower = totalPower * (1 - pitchBias)
  rearPower = totalPower * pitchBias
  print(frontPower, rearPower)


  MotorDrive.setMotorValue(mFrontLeft, frontPower * rollBias)
  setMotor(mFrontRight, frontPower * (1 - rollBias))

  setMotor(mBackLeft, rearPower * rollBias)
  setMotor(mBackRight, rearPower * (1 - rollBias))

  sleep(0.05)



