"""
Raspberry Pi Camp - Day 2 - Level 1 (guided build)
Alternating LEDs wrapped in a function, then a Tkinter GUI with 3 brightness
sliders, a buzzer volume slider, and a master on/off button.

Note: this matches Day 2 exactly as taught. The sliders do NOT check the
master switch yet, that bug gets found and fixed on Day 3, see
day3_level1a_fixed_sliders.py for the corrected version.

Wiring:
    LED 1  -> GPIO 17
    LED 2  -> GPIO 27
    LED 3  -> GPIO 22
    Buzzer -> GPIO 23
    Master button -> GPIO 2
"""

import tkinter as tk
from gpiozero import LED, PWMLED, PWMOutputDevice, Button
from time import sleep

# --- Part 1: alternating LEDs, wrapped in a function (morning demo) ---


def swap_leds(led_a, led_b, times=10):
    for i in range(times):
        led_a.on()
        led_b.off()
        sleep(0.5)
        led_a.off()
        led_b.on()
        sleep(0.5)


# Uncomment to run the morning demo on its own:
# demo_led1 = LED(17)
# demo_led2 = LED(27)
# swap_leds(demo_led1, demo_led2)
# demo_led1.close()
# demo_led2.close()


# --- Part 2: the full GUI control panel (afternoon build) ---

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

    s = tk.Scale(window, from_=0, to=100, orient="horizontal", command=set_val)
    s.pack()


make_slider(led1, "LED 1")
make_slider(led2, "LED 2")
make_slider(led3, "LED 3")


def set_volume(val):
    buzzer.value = int(val) / 100


tk.Label(window, text="Buzzer Volume").pack()
vol_slider = tk.Scale(window, from_=0, to=100, orient="horizontal", command=set_volume)
vol_slider.pack()

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
