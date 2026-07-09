"""
Raspberry Pi Camp - DIY Day - Reaction Game Extension: Catch a False Start
Pressing your button during "Get Ready..." now ends the round immediately
and hands the win to the other player.

Same wiring as day5_reaction_game.py.
"""

import random
from time import sleep, time
from gpiozero import LED, Button
from RPLCD.i2c import CharLCD

led = LED(17)
button1 = Button(27)
button2 = Button(22)
lcd = CharLCD('PCF8574', 0x27)


def play_round():
    lcd.clear()
    lcd.write_string('Get Ready...')

    wait_time = random.uniform(2, 5)
    start = time()
    false_start = None

    while time() - start < wait_time:
        if button1.is_pressed:
            false_start = "Player 1"
            break
        elif button2.is_pressed:
            false_start = "Player 2"
            break

    if false_start is not None:
        other = "Player 2" if false_start == "Player 1" else "Player 1"
        lcd.clear()
        lcd.write_string(false_start + " false start!")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(other + " wins!")
        return

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
