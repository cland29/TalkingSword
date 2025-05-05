from abc import ABC, abstractmethod

import adafruit_bno055
from adafruit_extended_bus import ExtendedI2C as I2C

i2c = I2C(1)

class Gyro(ABC):
    @abstractmethod
    def get_x(self) -> float:
        pass

    @abstractmethod
    def get_y(self) -> float:
        pass

    @abstractmethod
    def get_z(self) -> float:
        pass

class AdafruitBno055(Gyro):
    def __init__(self, id):
        self.sensor = adafruit_bno055.BNO055_I2C(i2c, id)

    def get_x(self) -> float:
        return self.sensor.eular[0]

    def get_y(self) -> float:
        return self.sensor.eular[1]
    
    def get_z(self) -> float:
        return self.sensor.eular[2]