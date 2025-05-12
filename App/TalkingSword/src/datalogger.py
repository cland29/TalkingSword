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
from datetime import datetime
import csv

from Hardware.accelerometer import *
from Constants.HardwareMap import BLADE_ACCELEROMETER_ID, HANDLE_ACCELEROMETER_ID
# To enable i2c-gpio, add the line `dtoverlay=i2c-gpio` to /boot/config.txt
# Then reboot the pi

# Create library object using our Extended Bus I2C port
# Use `ls /dev/i2c*` to find out what i2c devices are connected
i2c = I2C(1)

sensor = adafruit_bno055.BNO055_I2C(i2c, 0x28)

#accelerometer_1 = adafruit_adxl34x.ADXL345(i2c, 0x1d)
blade_accelerometer = AdafruitAdxl34x(BLADE_ACCELEROMETER_ID)
handle_acclerometer = AdafruitAdxl34x(HANDLE_ACCELEROMETER_ID)

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=1024)

duration=1

def get_current_datetime_string() -> str:
    """
    Returns the current date and time up to the nearest minute as a formatted string.
    Format: YYYY-MM-DD HH:MM
    """
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M")

def save_sensor_data_to_csv(file_path: str, sensor, handle_acclerometer, blade_accelerometer) -> None:
    """
    Saves sensor data to a new line in the specified CSV file.

    Args:
        file_path (str): The path to the CSV file.
        sensor: The sensor object with data attributes.
        handle_acclerometer: The handle accelerometer object.
        blade_accelerometer: The blade accelerometer object.
    """
    data = [
        get_current_datetime_string(),
        sensor.acceleration,
        sensor.magnetic,
        sensor.gyro,
        sensor.euler,
        sensor.quaternion,
        sensor.linear_acceleration,
        sensor.gravity,
        handle_acclerometer.get_x(),
        handle_acclerometer.get_y(),
        handle_acclerometer.get_z(),
        blade_accelerometer.get_x(),
        blade_accelerometer.get_y(),
        blade_accelerometer.get_z()
    ]

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

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

generate_tone(440, 1)

lock = threading.Lock()

def hit_threshold():
    while True:
        try:
            with lock:
             
             if blade_accelerometer.get_x() > 4:
              print(f"Stab")
              generate_tone(560, 0.1)
             elif blade_accelerometer.get_y() > 4:
              print(f"Slash")
              generate_tone(240, 0.1)
             elif blade_accelerometer.get_z() > 4:
              print(f"Slash")
              generate_tone(860, 0.1)
             else:
              print("False")
        except Exception as e:
            print(f"double")
        time.sleep(0.1)
def print_sensor():
 while True:
     #try:
       with lock:  
        save_sensor_data_to_csv(f"datafiles/{get_current_datetime_string()}.csv", handle_acclerometer=handle_acclerometer, blade_accelerometer=blade_accelerometer)
     #except Exception as e:
         #print(f"dooble?")
        time.sleep(1)

sum = 0
while sum < 30:
   sum += 1

   print_sensor()


#hit_threshold_thread = threading.Thread(target=hit_threshold)
#print_sensor_thread = threading.Thread(target=print_sensor)

# Start both threads
#hit_threshold_thread.start()
#print_sensor_thread.start()

# Main thread will continue running
#hit_threshold_thread.join()
#print_sensor_thread.join()

 