"""
Raspberry Pi Camp - Day 4 - Level 2 (independent challenge)
A GUI photo booth with clickable filter buttons (built from a dictionary,
so adding a filter is a one-line change) and a physical shutter button.

Wiring:
    Shutter button -> GPIO 27, GND
    Camera         -> CSI port
"""

import tkinter as tk
from gpiozero import Button as PiButton
from picamera2 import Picamera2
from PIL import Image, ImageTk, ImageOps
from datetime import datetime


def sepia(image):
    gray = ImageOps.grayscale(image)
    return ImageOps.colorize(gray, black="#3f2f1e", white="#f4e1c1")


filters = {"Grayscale": ImageOps.grayscale, "Sepia": sepia}
current_filter = ImageOps.grayscale

camera = Picamera2()
camera.start()

window = tk.Tk()
window.title("Photo Booth")
photo_label = tk.Label(window)
photo_label.pack()


def set_filter(f):
    global current_filter
    current_filter = f


for name, func in filters.items():
    tk.Button(window, text=name,
              command=lambda f=func: set_filter(f)).pack(side="left")


def take_photo():
    filename = datetime.now().strftime("booth_%H%M%S.jpg")
    camera.capture_file(filename)
    img = Image.open(filename)
    filtered = current_filter(img)
    display_img = ImageTk.PhotoImage(filtered.resize((320, 240)))
    photo_label.config(image=display_img)
    photo_label.image = display_img  # keep a reference or Tkinter drops it


shutter = PiButton(27)
# gpiozero callbacks fire on a background thread, hand off to Tkinter safely:
shutter.when_pressed = lambda: window.after(0, take_photo)

window.mainloop()
