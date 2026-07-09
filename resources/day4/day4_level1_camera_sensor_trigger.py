"""
Raspberry Pi Camp - Day 4 - Level 1 (guided build)
Automatically takes a photo when someone steps within range of the
ultrasonic sensor. A system LED and toggle button arm/disarm the whole thing.

Wiring:
    LED           -> GPIO 17
    Toggle button -> GPIO 22, GND
    Sensor        -> 5V, GND, Trigger on GPIO 23, Echo on GPIO 24
    Camera        -> CSI port
"""

from gpiozero import LED, Button, DistanceSensor
from picamera2 import Picamera2
from time import sleep
from datetime import datetime

camera = Picamera2()
camera.start()

sensor = DistanceSensor(echo=24, trigger=23)
led = LED(17)
toggle_button = Button(22)
system_on = True


def toggle_system():
    global system_on
    system_on = not system_on


toggle_button.when_pressed = toggle_system

print("Booth armed. Step within 30cm to trigger a photo. Ctrl+C to quit.")

while True:
    if system_on:
        led.on()
        cm = sensor.distance * 100
        if cm < 30:
            filename = datetime.now().strftime("photo_%H%M%S.jpg")
            camera.capture_file(filename)
            print("Captured:", filename)
            sleep(3)  # cooldown so one visit doesn't spam captures
    else:
        led.off()
    sleep(0.1)
