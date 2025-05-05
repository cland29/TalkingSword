from abc import ABC, abstractmethod

import adafruit_adxl34x
from adafruit_extended_bus import ExtendedI2C as I2C

i2c = I2C(1)

class Accelerometer(ABC):
    @abstractmethod
    def get_x(self) -> float:
        pass

    @abstractmethod
    def get_y(self) -> float:
        pass

    @abstractmethod
    def get_z(self) -> float:
        pass

class AdafruitAdxl34x(Accelerometer):
    def __init__(self, id):
        self.accel = adafruit_adxl34x.ADXL345(i2c, id)

    def get_x(self) -> float:
        return self.accel.acceleration[0]
    
    def get_y(self) -> float:
        return self.accel.acceleration[1]
    
    def get_z(self) -> float:
        return self.accel.acceleration[2]

