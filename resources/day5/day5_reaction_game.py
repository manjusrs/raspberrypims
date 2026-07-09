"""
Raspberry Pi Camp - DIY Day - Reaction Game (base build)
An LED flashes after a random delay. Whoever presses their button first
wins, and the LCD shows who won and how fast.

Wiring:
    LED         -> GPIO 17
    P1 button   -> GPIO 27, GND
    P2 button   -> GPIO 22, GND
    LCD         -> 5V, GND, SDA, SCL (I2C)
"""

import random
from time import sleep, time
from gpiozero import LED, Button
from RPLCD.i2c import CharLCD

led = LED(17)
button1 = Button(27)
button2 = Button(22)
lcd = CharLCD('PCF8574', 0x27)  # change to your i2cdetect address if different


def play_round():
    lcd.clear()
    lcd.write_string('Get Ready...')
    sleep(random.uniform(2, 5))

    led.on()
    lcd.clear()
    lcd.write_string('GO!')
    start_time = time()

    winner = None
    while winner is None:
        if button1.is_pressed:
            winner = "Player 1"
        elif button2.is_pressed:
            winner = "Player 2"

    elapsed = time() - start_time
    led.off()
    lcd.clear()
    lcd.write_string(winner + " wins!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f"Time: {elapsed:.2f}s")


play_round()
again = input("Play again? (y/n): ")
while again == "y":
    play_round()
    again = input("Play again? (y/n): ")

print("Thanks for playing!")
