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
  if value >= 1:
      value = 1
  motor.value = value

def getPitchBias(currentBias):
    error = pitch()
    pitchPID.update(error)

    return pitchPID.output


totalPower = 0.1
rollCalibration = 0
pitchCalibration = 0
rollCalibration = roll()
pitchCalibration = pitch()

pitchPID = PID.PID(0.2, 0, 0)
pitchPID.SetPoint=0.0
pitchPID.setSampleTime(0.01)

pitchBias = 0.5

while(True):
  pitchBias += getPitchBias() * 0.1
  frontPower = totalPower * pitchBias
  rearPower = totalPower * (1 - pitchBias)

  print(frontPower, rearPower)


  setMotor(frontLeftMotor, frontPower)
  setMotor(frontRightMotor, frontPower)

  setMotor(rearLeftMotor, rearPower)
  setMotor(rearRightMotor, rearPower)

  sleep(0.01)
