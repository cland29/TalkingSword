# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example demonstrates how to instantiate the
Adafruit BNO055 Sensor using this library 
"""

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
import adafruit_adxl34x

# To enable i2c-gpio, add the line `dtoverlay=i2c-gpio` to /boot/config.txt
# Then reboot the pi

# Create library object using our Extended Bus I2C port
# Use `ls /dev/i2c*` to find out what i2c devices are connected
i2c = I2C(1)

sensor = adafruit_bno055.BNO055_I2C(0x28)

"last_val = 0xFFFF"
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
 print(f"Temperature: {temperature()} degrees C")
 print(f"Accelerometer (m/s^2): {sensor.acceleration}")
 print(f"Magnetometer (microteslas): {sensor.magnetic}")
 print(f"Gyroscope (rad/sec): {sensor.gyro}")
 print(f"Euler angle: {sensor.euler}")
 print(f"Quaternion: {sensor.quaternion}")
 print(f"Linear acceleration (m/s^2): {sensor.linear_acceleration}")
 print(f"Gravity (m/s^2): {sensor.gravity}")
 print(f"accel 1: {accelerometer_1.acceleration[0]} {accelerometer_1.acceleration[1]} {accelerometer_1.acceleration[2]}")
 print(f"accel 2: {accelerometer_2.acceleration[0]} {accelerometer_2.acceleration[1]} {accelerometer_2.acceleration[2]}")
