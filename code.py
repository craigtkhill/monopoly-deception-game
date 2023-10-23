from adafruit_circuitplayground import cp
import random
import time

# Constants
BRIGHTNESS = 0.1
TIMER_INTERVAL = (1, 2)
NUM_ROUNDS = 2
MAX_PLAYERS = 8
FLASH_DELAY = 0.1
BUTTON_DEBOUNCE = 0.2

# Colors for players
ALL_COLORS = [
    (0, 0, 255), (0, 255, 0), (255, 255, 0),
    (0, 255, 255), (255, 0, 255), (255, 0, 0),
    (255,255,255), (255, 50, 0)
]

# Variables
num_players = MAX_PLAYERS
current_round = 0
current_pixel = 0
round_colors = []

# Initialize brightness
cp.pixels.brightness = BRIGHTNESS

def play_tone(frequency, duration):
    cp.play_tone(frequency, duration)

def display_colors():
    for i in range(num_players):
        cp.pixels[i] = ALL_COLORS[i]
    for i in range(num_players, len(cp.pixels)):
        cp.pixels[i] = (0, 0, 0)
    cp.pixels.show()

def flash_color(color, times):
    for _ in range(times):
        cp.pixels.fill(color)
        cp.pixels.show()
        time.sleep(FLASH_DELAY)
        cp.pixels.fill((0, 0, 0))
        cp.pixels.show()
        time.sleep(FLASH_DELAY)

def wait_for_button():
    print("Waiting for button press...")
    while not cp.button_a and not cp.button_b:
        time.sleep(0.1)
    print("Button pressed!")
    time.sleep(BUTTON_DEBOUNCE)  # debounce

# Setup phase
display_colors()

# Game start phase
while True:
    if cp.button_a:
        num_players = max(1, num_players - 1) if num_players > 1 else MAX_PLAYERS
        display_colors()
    elif cp.button_b:
        print("Game starting!")
        break
    time.sleep(0.1)

# Clear the pixels before starting the game
cp.pixels.fill((0, 0, 0))
cp.pixels.show()

# Game phase
colors = ALL_COLORS[:num_players]
while current_round < NUM_ROUNDS:
    color = random.choice(colors)
    round_colors.append(color)

    interval = random.randint(*TIMER_INTERVAL)

    cp.pixels[current_pixel] = color
    cp.pixels.show()
    time.sleep(interval)

    current_pixel += 1 if random.random() >= 0.1 or current_pixel == 0 else -1

    if current_pixel >= len(cp.pixels):
        play_tone(880, 1)
        current_pixel = 0
        current_round += 1

        if current_round <= NUM_ROUNDS:
            color_counts = {color: round_colors.count(color) for color in colors}
            max_count = max(color_counts.values())
            most_common_colors = [color for color, count in color_counts.items() if count == max_count]

            winning_color = random.choice(most_common_colors)
            print(f"Round {current_round} winner's color is {winning_color}!")

            print("Flashing winning color until button press...")
            while not cp.button_a and not cp.button_b:
                flash_color(winning_color, 1)

            round_colors = []
            cp.pixels.fill((0, 0, 0))
            cp.pixels.show()

# Game over phase
while True:
    cp.pixels.fill((255, 0, 0))
