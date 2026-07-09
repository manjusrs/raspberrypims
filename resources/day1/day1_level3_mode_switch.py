"""
Raspberry Pi Camp - Day 1 - Level 3 (hardest independent challenge)
A button cycles the LED through three modes: off, solid, and breathing fade.

Wiring:
    LED    -> GPIO 17 (through a resistor) -> GND
    Button -> GPIO 2 -> GND
"""

from gpiozero import PWMLED, Button
from time import sleep

led = PWMLED(17)
button = Button(2)
mode = 0  # 0 = off, 1 = solid, 2 = breathing fade


def next_mode():
    global mode
    mode = (mode + 1) % 3


button.when_pressed = next_mode

brightness = 0
direction = 1

while True:
    if mode == 0:
        led.value = 0
    elif mode == 1:
        led.value = 1
    elif mode == 2:
        brightness += direction * 0.02
        if brightness >= 1 or brightness <= 0:
            direction *= -1
        led.value = max(0, min(1, brightness))
    sleep(0.02)
