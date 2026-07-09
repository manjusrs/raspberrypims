"""
Raspberry Pi Camp - Day 3 - Level 2 (independent challenge)
Same threshold logic as Part B, but alerts with a buzzer instead of an LED.

Wiring:
    Sensor -> 5V, GND, Trigger on GPIO 23, Echo on GPIO 24
    Buzzer -> GPIO 27, GND
"""

import tkinter as tk
from gpiozero import DistanceSensor, Buzzer

sensor = DistanceSensor(echo=24, trigger=23)
buzzer = Buzzer(27)
system_on = True

window = tk.Tk()
label = tk.Label(window, text="-- cm", font=("Arial", 32))
label.pack()


def check_sensor():
    if system_on:
        cm = sensor.distance * 100
        label.config(text=f"{cm:.1f} cm")
        if cm < 15:
            buzzer.on()
        else:
            buzzer.off()
    window.after(200, check_sensor)


def toggle_system():
    global system_on
    system_on = not system_on
    if not system_on:
        buzzer.off()
        label.config(text="OFF")


tk.Button(window, text="On/Off", command=toggle_system).pack()

check_sensor()
window.mainloop()
