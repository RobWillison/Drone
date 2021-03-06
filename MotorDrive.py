import smbus, time

MOTOR1 = 0x08
MOTOR2 = 0x0C
MOTOR3 = 0x10
MOTOR4 = 0x14

I2C_ADDR = 0x40

MAX = 1664
MIN = 836

def getBus():
    return smbus.SMBus(1)

def setup():
    bus = getBus()
    bus.write_byte_data(I2C_ADDR, 0, 0x20)
    bus.write_byte_data(I2C_ADDR, 0xfe, 0x1e)

    bus.write_word_data(I2C_ADDR, 0x06, 0)
    bus.write_word_data(I2C_ADDR, 0x0A, 0)
    bus.write_word_data(I2C_ADDR, 0x0E, 0)
    bus.write_word_data(I2C_ADDR, 0x12, 0)

# Value is between 0 and 100
def setMotorValue(motor, value):
    bus = getBus()
    value = MIN + (value / 100.0) * (MAX - MIN)
    bus.write_word_data(I2C_ADDR, motor, int(value))

def motor1(value):
    setMotorValue(MOTOR1, value)

def motor2(value):
    setMotorValue(MOTOR2, value)

def motor3(value):
    setMotorValue(MOTOR3, value)

def motor4(value):
    setMotorValue(MOTOR4, value)