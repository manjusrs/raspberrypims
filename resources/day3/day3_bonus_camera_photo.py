"""
Raspberry Pi Camp - Day 3 - Bonus
Wires the Pi Camera to a GUI button that takes a timestamped photo.

Wiring: camera ribbon cable into the CSI port (not GPIO).
"""

import tkinter as tk
from picamera2 import Picamera2
from datetime import datetime

camera = Picamera2()
camera.start()

window = tk.Tk()
status = tk.Label(window, text="Ready")
status.pack()


def take_photo():
    filename = datetime.now().strftime("photo_%H%M%S.jpg")
    camera.capture_file(filename)
    status.config(text=f"Saved {filename}")


tk.Button(window, text="Take Photo", command=take_photo).pack()

window.mainloop()
