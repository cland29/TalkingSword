from gpiozero import LED
from time import sleep

led = LED(47)

print("Hello world")

count = 0

while count < 10:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    count += 1