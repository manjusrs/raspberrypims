"""
Raspberry Pi Camp - Day 2 - Level 3 (hardest independent challenge)
The buzzer's volume automatically tracks the average brightness of the
3 LEDs, live, with no separate volume slider. One function is called from
all three LED sliders to keep the buzzer updated.

Builds on day2_level1_functions_gui.py. Same wiring.
"""

import tkinter as tk
from gpiozero import PWMLED, PWMOutputDevice, Button

led1 = PWMLED(17)
led2 = PWMLED(27)
led3 = PWMLED(22)
buzzer = PWMOutputDevice(23)

window = tk.Tk()
window.title("LED Control Panel")


def update_buzzer():
    average = (led1.value + led2.value + led3.value) / 3
    buzzer.value = average


def set_led1(val):
    led1.value = int(val) / 100
    update_buzzer()


def set_led2(val):
    led2.value = int(val) / 100
    update_buzzer()


def set_led3(val):
    led3.value = int(val) / 100
    update_buzzer()


tk.Label(window, text="LED 1").pack()
tk.Scale(window, from_=0, to=100, orient="horizontal", command=set_led1).pack()

tk.Label(window, text="LED 2").pack()
tk.Scale(window, from_=0, to=100, orient="horizontal", command=set_led2).pack()

tk.Label(window, text="LED 3").pack()
tk.Scale(window, from_=0, to=100, orient="horizontal", command=set_led3).pack()


button = Button(2)
system_on = True


def toggle_system():
    global system_on
    system_on = not system_on
    if not system_on:
        led1.off()
        led2.off()
        led3.off()
        buzzer.off()


button.when_pressed = toggle_system

window.mainloop()
