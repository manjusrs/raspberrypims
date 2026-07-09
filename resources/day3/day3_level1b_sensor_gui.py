"""
Raspberry Pi Camp - Day 3 - Level 1, Part B (guided build)
A single LED plus an ultrasonic distance sensor. A GUI shows the live
distance in cm and lights the LED whenever something is within 15cm.

Wiring:
    LED     -> GPIO 17
    Sensor  -> 5V, GND, Trigger on GPIO 23, Echo on GPIO 24
"""

import tkinter as tk
from gpiozero import DistanceSensor, LED

sensor = DistanceSensor(echo=24, trigger=23)
led = LED(17)
system_on = True

window = tk.Tk()
label = tk.Label(window, text="-- cm", font=("Arial", 32))
label.pack()


def check_sensor():
    if system_on:
        cm = sensor.distance * 100
        label.config(text=f"{cm:.1f} cm")
        if cm < 15:
            led.on()
        else:
            led.off()
    window.after(200, check_sensor)


def toggle_system():
    global system_on
    system_on = not system_on
    if not system_on:
        led.off()
        label.config(text="OFF")


tk.Button(window, text="On/Off", command=toggle_system).pack()

check_sensor()
window.mainloop()
