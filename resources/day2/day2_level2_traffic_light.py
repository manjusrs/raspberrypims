"""
Raspberry Pi Camp - Day 2 - Level 2 (independent challenge)
Adds a "Traffic Light Mode" button that automatically cycles the 3 LEDs
through a real red -> green -> yellow -> red sequence, using window.after()
instead of sleep() so the GUI never freezes.

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


def make_slider(led, label):
    tk.Label(window, text=label).pack()

    def set_val(val):
        led.value = int(val) / 100

    tk.Scale(window, from_=0, to=100, orient="horizontal", command=set_val).pack()


make_slider(led1, "LED 1")
make_slider(led2, "LED 2")
make_slider(led3, "LED 3")


def set_volume(val):
    buzzer.value = int(val) / 100


tk.Label(window, text="Buzzer Volume").pack()
tk.Scale(window, from_=0, to=100, orient="horizontal", command=set_volume).pack()


# --- Traffic light mode ---

def show_red():
    led1.value = 1
    led2.value = 0
    led3.value = 0
    window.after(2000, show_green)


def show_green():
    led1.value = 0
    led2.value = 0
    led3.value = 1
    window.after(2000, show_yellow)


def show_yellow():
    led1.value = 0
    led2.value = 1
    led3.value = 0
    window.after(500, show_red)


tk.Button(window, text="Traffic Light Mode", command=show_red).pack()


# --- Master button ---

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
