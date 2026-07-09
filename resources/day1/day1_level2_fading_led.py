"""
Raspberry Pi Camp - Day 1 - Level 2 (independent challenge)
Make the LED breathe: fade smoothly from off to full brightness and back.

Wiring: same LED circuit as Level 1, on GPIO 17.
"""

from gpiozero import PWMLED
from time import sleep

led = PWMLED(17)

while True:
    for i in range(0, 11):
        led.value = i / 10
        sleep(0.05)
    for i in range(10, -1, -1):
        led.value = i / 10
        sleep(0.05)
