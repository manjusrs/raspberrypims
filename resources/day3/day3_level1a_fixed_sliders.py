"""
Raspberry Pi Camp - Day 3 - Level 1, Part A (guided fix)
Fixes yesterday's bug: sliders now check system_on before touching any LED
or the buzzer. Also adds colored slider troughs matching each LED.

Same wiring as Day 2.
"""

import tkinter as tk
from gpiozero import PWMLED, PWMOutputDevice, Button

led1 = PWMLED(17)
led2 = PWMLED(27)
led3 = PWMLED(22)
buzzer = PWMOutputDevice(23)
system_on = True

window = tk.Tk()
window.title("LED Control Panel")


def set_led1(val):
    if system_on:
        led1.value = int(val) / 100


def set_led2(val):
    if system_on:
        led2.value = int(val) / 100


def set_led3(val):
    if system_on:
        led3.value = int(val) / 100


def set_volume(val):
    if system_on:
        buzzer.value = int(val) / 100


tk.Scale(window, from_=0, to=100, orient="horizontal",
         troughcolor="red", label="LED 1", command=set_led1).pack()

tk.Scale(window, from_=0, to=100, orient="horizontal",
         troughcolor="#e6b800", label="LED 2", command=set_led2).pack()

tk.Scale(window, from_=0, to=100, orient="horizontal",
         troughcolor="green", label="LED 3", command=set_led3).pack()

tk.Scale(window, from_=0, to=100, orient="horizontal",
         troughcolor="gray", label="Buzzer Volume", command=set_volume).pack()

button = Button(2)


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
