# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example demonstrates how to instantiate the
Adafruit BNO055 Sensor using this library and just
the I2C bus number.
This example will only work on a Raspberry Pi
and does require the i2c-gpio kernel module to be
installed and enabled. Most Raspberry Pis will
already have it installed, however most do not
have it enabled. You will have to manually enable it
"""

import time
from adafruit_extended_bus 
"import ExtendedI2C as I2C"
import adafruit_bno055
import adafruit_adxl34x

# To enable i2c-gpio, add the line `dtoverlay=i2c-gpio` to /boot/config.txt
# Then reboot the pi

# Create library object using our Extended Bus I2C port
# Use `ls /dev/i2c*` to find out what i2c devices are connected


sensor = adafruit_bno055.BNO055_I2C(0x28)

last_val = 0xFFFF
accelerometer_1 = adafruit_adxl34x.ADXL345(0x1d)
accelerometer_2 = adafruit_adxl34x.ADXL345(0x53)

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


while True:
    print("Temperature: {} degrees C".format(temperature()))
    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    print("Gravity (m/s^2): {}".format(sensor.gravity))
    print("222")
    print("%f %f %f"%accelerometer_1.acceleration)
    print("%f %f %f"%accelerometer_2.acceleration)
    time.sleep(1)
