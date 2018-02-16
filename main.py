import Adafruit_LSM9DS0
from gpiozero import Motor, OutputDevice
from time import sleep
import math

rearRightMotor = Motor(27, 24)
motor1_enable = OutputDevice(5, initial_value=1)
rearLeftMotor = Motor(6, 22)
motor2_enable = OutputDevice(17, initial_value=1)
frontLeftMotor = Motor(23, 16)
motor3_enable = OutputDevice(12, initial_value=1)
frontRightMotor = Motor(13, 18)
motor4_enable = OutputDevice(25, initial_value=1)

imu = Adafruit_LSM9DS0.LSM9DS0()

def pitch():
  (mag_x, mag_y, mag_z) = imu.readMag()
  (acc_x, acc_y, acc_z) = imu.readAccel()

  # Normalising the accelerometer data
  # Dividing variable (don't know why I use this)
  acc_norm_div = math.sqrt(acc_x**2 + acc_y**2 + acc_z**2)

  # Normalised values
  acc_x_norm = acc_x / acc_norm_div
  acc_y_norm = acc_y / acc_norm_div

  # Calc pitch and roll using trig
  pitch = math.asin(acc_x_norm)

  return pitch

def roll():
  (mag_x, mag_y, mag_z) = imu.readMag()
  (acc_x, acc_y, acc_z) = imu.readAccel()

  # Normalising the accelerometer data
  # Dividing variable (don't know why I use this)
  acc_norm_div = math.sqrt(acc_x**2 + acc_y**2 + acc_z**2)

  # Normalised values
  acc_x_norm = acc_x / acc_norm_div
  acc_y_norm = acc_y / acc_norm_div

  # Calc pitch and roll using trig#
  pitch = math.asin(acc_x_norm)
  roll = - math.asin(math.radians(acc_y_norm / math.cos(pitch)))

  return roll

def getRollBias():
  rollAngle = roll() - rollCalibration
  bias = (rollAngle / 180) + 0.5

  return bias

def getPitchBias():
  pitchAngle = pitch() - pitchCalibration
  bias = (pitchAngle / 180) + 0.5

  return bias

totalPower = 0.1
rollCalibration = roll()
pitchCalibration = pitch()

while(True):
  pitchBias = getPitchBias()
  rollBias = getRollBias()
  frontPower = totalPower * pitchBias
  rearPower = totalPower * (1 - pitchBias)

  frontLeftMotor.value = frontPower * rollBias
  frontRightMotor.value = frontPower * (1 - rollBias)

  rearLeftMotor.value = rearPower * rollBias
  rearRightMotor.value = rearPower * (1 - rollBias)

  sleep(0.05)



