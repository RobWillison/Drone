import Adafruit_LSM9DS0
from gpiozero import Motor, OutputDevice
from time import sleep
import math
import PID

rearRightMotor = Motor(27, 24)
motor1_enable = OutputDevice(5, initial_value=1)
rearLeftMotor = Motor(6, 22)
motor2_enable = OutputDevice(17, initial_value=1)
frontLeftMotor = Motor(23, 16)
motor3_enable = OutputDevice(12, initial_value=1)
frontRightMotor = Motor(13, 18)
motor4_enable = OutputDevice(25, initial_value=1)

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


throttle = 0.1
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

  leftAdjust = getRollBias() * 0.01
  rightAdjust = - getRollBias() * 0.01

  setMotor(frontLeftMotor, throttle + frontAdjust + leftAdjust)
  setMotor(frontRightMotor, throttle + frontAdjust + rightAdjust)

  setMotor(rearLeftMotor, throttle + rearAdjust + leftAdjust)
  setMotor(rearRightMotor, throttle + rearAdjust + rightAdjust)

  sleep(0.0001)
