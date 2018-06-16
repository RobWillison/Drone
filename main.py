import Adafruit_LSM9DS0
import MotorDrive
from time import sleep
import math
import PID
import redis

MotorDrive.setup()

mFrontLeft = MotorDrive.MOTOR4
mFrontRight = MotorDrive.MOTOR2
mBackLeft = MotorDrive.MOTOR41
mBackRight = MotorDrive.MOTOR3
motorTrim = [0, 50, 0, 0]
imu = Adafruit_LSM9DS0.LSM9DS0()

fXg = 0
fYg = 0
fZg = 0
alpha = 0.5

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

def clamp(n, minn, maxn):
  if n < minn:
    return minn
  elif n > maxn:
    return maxn
  else:
    return n

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
  redisClient.set('pitch', str(math.degrees(pitch)))
  return math.degrees(pitch)

def roll():
  Xg, Yg, Zg = filterAccel()

  roll = math.atan2(-Yg, Zg)
  return math.degrees(roll)

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

throttle = 30
pitchPID = PID.PID(0.2, 0, 0)
pitchPID.SetPoint=0.0
pitchPID.setSampleTime(0.0001)

rollPID = PID.PID(0.5, 0.01, 0.01)
rollPID.SetPoint=0.0
rollPID.setSampleTime(0.0001)

while(True):
  pitchAdjust = clamp(- getPitchBias(), -100, 100)
  print(pitchAdjust)
  # leftAdjust = getRollBias() * 0.01
  # rightAdjust = - getRollBias() * 0.01

  MotorDrive.setMotorValue(mFrontLeft, throttle + motorTrim[0] + pitchAdjust)
  MotorDrive.setMotorValue(mFrontRight, throttle + motorTrim[1] + pitchAdjust)

  MotorDrive.setMotorValue(mBackLeft, throttle + motorTrim[2] - pitchAdjust)
  MotorDrive.setMotorValue(mBackRight, throttle + motorTrim[3] - pitchAdjust)

  sleep(0.0001)                                                                                                                                                                                              61        1,1           To