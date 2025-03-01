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
import sys
import pygame
import os
import numpy as np
import threading

# To enable i2c-gpio, add the line `dtoverlay=i2c-gpio` to /boot/config.txt
# Then reboot the pi

# Create library object using our Extended Bus I2C port
# Use `ls /dev/i2c*` to find out what i2c devices are connected
i2c = I2C(1)

sensor = adafruit_bno055.BNO055_I2C(i2c, 0x28)

accelerometer_1 = adafruit_adxl34x.ADXL345(i2c, 0x1d)
accelerometer_2 = adafruit_adxl34x.ADXL345(i2c, 0x53)

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=1024)

duration=1

def generate_tone(frequency, duration, volume=1):
    sample_rate = 44100  # 44.1 kHz sample rate
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)

    wave = np.sin(2 * np.pi * frequency * t)  # Generate sine wave
    wave = (wave * 32767).astype(np.int16)  # Convert to 16-bit PCM format

    sound = pygame.sndarray.make_sound(wave)
    sound.set_volume(volume)
    sound.play()

pygame.time.delay(int(duration * 1000))  # Wait for sound to finish

generate_tone(440, 2)

lock = threading.Lock()

def hit_threshold():
    while True:
        try:
            with lock:
             x2,y2,z2 =accelerometer_2.acceleration
             if x2 > 2:
              print(f"TRUE")
              generate_tone(560, 1)
        except Exception as e:
            print(f"double")
        time.sleep(0.1)
def print_sensor():
 while True:
     try:
       with lock:  
        print("\033c", end="")

        print(f"Accelerometer (m/s^2): {sensor.acceleration}")
        print(f"Magnetometer (microteslas): {sensor.magnetic}")
        print(f"Gyroscope (rad/sec): {sensor.gyro}")
        print(f"Euler angle: {sensor.euler}")
        print(f"Quaternion: {sensor.quaternion}")
        print(f"Linear acceleration (m/s^2): {sensor.linear_acceleration}")
        print(f"Gravity (m/s^2): {sensor.gravity}")
        print(f"accel 1: {accelerometer_1.acceleration[0]} {accelerometer_1.acceleration[1]} {accelerometer_1.acceleration[2]}")
        print(f"accel 2: {accelerometer_2.acceleration[0]} {accelerometer_2.acceleration[1]} {accelerometer_2.acceleration[2]}")
     except Exception as e:
         print(f"dooble")
     time.sleep(0.5)

hit_threshold_thread = threading.Thread(target=hit_threshold)
print_sensor_thread = threading.Thread(target=print_sensor)

# Start both threads
hit_threshold_thread.start()
print_sensor_thread.start()

# Main thread will continue running
hit_threshold_thread.join()
print_sensor_thread.join()

 