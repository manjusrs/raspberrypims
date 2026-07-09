"""
Raspberry Pi Camp - Day 3 - Level 3 (hardest independent challenge)
A real parking-sensor style alert: the buzzer beeps faster the closer your
hand gets, and goes silent beyond 50cm.

Wiring: same as Level 2.
"""

import tkinter as tk
from gpiozero import DistanceSensor, Buzzer

sensor = DistanceSensor(echo=24, trigger=23)
buzzer = Buzzer(27)
system_on = True

window = tk.Tk()
label = tk.Label(window, text="-- cm", font=("Arial", 32))
label.pack()


def distance_to_delay(cm):
    if cm > 50:
        return None
    return int(100 + (cm / 50) * 700)


def beep_cycle():
    if not system_on:
        window.after(200, beep_cycle)
        return
    cm = sensor.distance * 100
    label.config(text=f"{cm:.1f} cm")
    delay = distance_to_delay(cm)
    if delay is None:
        buzzer.off()
        window.after(200, beep_cycle)
    else:
        buzzer.on()
        window.after(50, buzzer.off)
        window.after(delay, beep_cycle)


def toggle_system():
    global system_on
    system_on = not system_on
    if not system_on:
        buzzer.off()
        label.config(text="OFF")


tk.Button(window, text="On/Off", command=toggle_system).pack()

beep_cycle()
window.mainloop()
