"""
Raspberry Pi Camp - Day 4 - Level 3 (hardest independent challenge)
Merges the morning's auto-trigger sensor with the afternoon's filterable
photo booth GUI. The booth fires automatically on approach, the physical
shutter still works as a manual override, and the system LED/toggle still
arms and disarms everything.

Wiring:
    LED            -> GPIO 17
    Toggle button  -> GPIO 22, GND
    Shutter button -> GPIO 27, GND
    Sensor         -> 5V, GND, Trigger on GPIO 23, Echo on GPIO 24
    Camera         -> CSI port
"""

import tkinter as tk
from gpiozero import LED, Button as PiButton, DistanceSensor
from picamera2 import Picamera2
from PIL import Image, ImageTk, ImageOps
from datetime import datetime
from time import time


def sepia(image):
    gray = ImageOps.grayscale(image)
    return ImageOps.colorize(gray, black="#3f2f1e", white="#f4e1c1")


filters = {"Grayscale": ImageOps.grayscale, "Sepia": sepia}
current_filter = ImageOps.grayscale

camera = Picamera2()
camera.start()
sensor = DistanceSensor(echo=24, trigger=23)
led = LED(17)
toggle_button = PiButton(22)
shutter = PiButton(27)
system_on = True

window = tk.Tk()
window.title("Smart Photo Booth")
photo_label = tk.Label(window)
photo_label.pack()


def set_filter(f):
    global current_filter
    current_filter = f


for name, func in filters.items():
    tk.Button(window, text=name,
              command=lambda f=func: set_filter(f)).pack(side="left")


def toggle_system():
    global system_on
    system_on = not system_on
    led.on() if system_on else led.off()


toggle_button.when_pressed = toggle_system


def take_photo():
    filename = datetime.now().strftime("booth_%H%M%S.jpg")
    camera.capture_file(filename)
    img = Image.open(filename)
    filtered = current_filter(img)
    display_img = ImageTk.PhotoImage(filtered.resize((320, 240)))
    photo_label.config(image=display_img)
    photo_label.image = display_img


shutter.when_pressed = lambda: window.after(0, take_photo)

last_capture = 0


def check_sensor():
    global last_capture
    if system_on:
        cm = sensor.distance * 100
        if cm < 30 and time() - last_capture > 3:
            take_photo()
            last_capture = time()
    window.after(200, check_sensor)


led.on()
check_sensor()
window.mainloop()
