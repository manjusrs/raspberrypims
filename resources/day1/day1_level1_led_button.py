"""
Raspberry Pi Camp - Day 1 - Level 1 (guided build)
Simple LED circuit, then adding a button.

Wiring:
    LED    -> GPIO 17 (through a resistor) -> GND
    Button -> GPIO 2 -> GND
"""

from gpiozero import LED, Button
from time import sleep
from signal import pause

led = LED(17)

# --- Step 1: turn the LED on and off ---
led.on()
sleep(1)
led.off()

# --- Step 2: make it blink ---
for i in range(10):
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)

# --- Step 3: add a button that controls the LED ---
button = Button(2)

button.when_pressed = led.on
button.when_released = led.off

print("Hold the button to light the LED. Press Ctrl+C to quit.")
pause()  # keeps the program alive so the button keeps working
