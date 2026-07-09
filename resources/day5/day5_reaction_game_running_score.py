"""
Raspberry Pi Camp - DIY Day - Reaction Game Extension: Running Score
Tracks wins across rounds and declares a champion at 3 wins.

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

    led.off()
    return winner, time() - start_time


p1_score = 0
p2_score = 0
champion = None

while champion is None:
    winner, elapsed = play_round()

    if winner == "Player 1":
        p1_score += 1
    else:
        p2_score += 1

    lcd.clear()
    lcd.write_string(winner + " wins!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f"P1:{p1_score}  P2:{p2_score}")
    sleep(2)

    if p1_score == 3 or p2_score == 3:
        champion = "Player 1" if p1_score == 3 else "Player 2"
        lcd.clear()
        lcd.write_string(champion + " wins the match!")

print(champion, "wins the match!")
