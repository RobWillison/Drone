import Adafruit_LSM9DS0
import MotorDrive
from time import sleep
import math
import PID

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

def setMotor(motor, value):
  if value <= 0:
    value = 0

  if value >= 1:
      value = 1
  motor.value = value

def getPitchBias():
    error = pitch()
    pitchPID.update(error)

    return pitchPID.output

def getRollBias():
    error = roll()
    rollPID.update(error)

    return rollPID.output


throttle = 50
rollCalibration = 0
pitchCalibration = 0
rollCalibration = roll()
pitchCalibration = pitch()

pitchPID = PID.PID(0.01, 0.01, 0.01)
pitchPID.SetPoint=0.0
pitchPID.setSampleTime(0.0001)

rollPID = PID.PID(0.01, 0.01, 0.01)
rollPID.SetPoint=0.0
rollPID.setSampleTime(0.0001)

while(True):
  frontAdjust = getPitchBias() * 0.01
  rearAdjust = - getPitchBias() * 0.01
  print(frontAdjust, rearAdjust)
  # leftAdjust = getRollBias() * 0.01
  # rightAdjust = - getRollBias() * 0.01

  # MotorDrive.setMotorValue(mFrontLeft, throttle + frontAdjust + leftAdjust)
  # MotorDrive.setMotorValue(mFrontRight, throttle + frontAdjust + rightAdjust)
  #
  # MotorDrive.setMotorValue(mBackLeft, throttle + rearAdjust + leftAdjust)
  # MotorDrive.setMotorValue(mBackRight, throttle + rearAdjust + rightAdjust)

  sleep(0.0001)
