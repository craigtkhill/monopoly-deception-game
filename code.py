from adafruit_circuitplayground import cp
import random
import time

# Constants
BRIGHTNESS = 0.1
NUM_ROUNDS = 20
MAX_PLAYERS = 8
FLASH_DELAY = 0.1
BUTTON_DEBOUNCE = 0.2
GAME_DURATION = 3600  # Game duration in seconds (1 hour)
START_INTERVAL = (
    GAME_DURATION / NUM_ROUNDS
)  # Average interval for each round at the start
MIN_INTERVAL = START_INTERVAL / 2  # Minimum interval by the end of the game
INTERVAL_DECREASE = (
    START_INTERVAL - MIN_INTERVAL
) / NUM_ROUNDS  # Decrease interval each round

# Colors for players
ALL_COLORS = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 0, 0),
    (255, 255, 255),
    (255, 50, 0),
]

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


# Main game loop
while True:
    # Variables that need to be reset at the start of each game
    game_start_time = time.monotonic()
    num_players = MAX_PLAYERS
    current_round = 0
    current_pixel = 0
    round_colors = []
    current_interval = START_INTERVAL

    display_colors()

    # Game start phase
    while True:
        if cp.button_a:
            time.sleep(BUTTON_DEBOUNCE)  # Button debounce delay
            num_players = max(1, num_players - 1) if num_players > 1 else MAX_PLAYERS
            display_colors()
        elif cp.button_b:
            time.sleep(BUTTON_DEBOUNCE)  # Button debounce delay
            print("Game starting!")
            break
        time.sleep(0.1)

    # Clear the pixels before starting the game
    cp.pixels.fill((0, 0, 0))
    cp.pixels.show()

    # Game phase
    colors = ALL_COLORS[:num_players]
    while current_round < NUM_ROUNDS:
        # Check if the game has been running for more than an hour
        if time.monotonic() - game_start_time >= GAME_DURATION:
            print("Game over, an hour has passed!")
            break

        interval = max(
            MIN_INTERVAL, current_interval - current_round * INTERVAL_DECREASE
        )
        color = random.choice(colors)
        round_colors.append(color)

        cp.pixels[current_pixel] = color
        cp.pixels.show()
        time.sleep(interval)

        current_pixel += 1 if random.random() >= 0.1 or current_pixel == 0 else -1

        if current_pixel >= len(cp.pixels):
            play_tone(220, 1)
            current_pixel = 0
            current_round += 1

            if current_round < NUM_ROUNDS:
                color_counts = {color: round_colors.count(color) for color in colors}
                max_count = max(color_counts.values())
                most_common_colors = [
                    color for color, count in color_counts.items() if count == max_count
                ]
                winning_color = random.choice(most_common_colors)

                print(f"Round {current_round} winner's color is {winning_color}!")
                print("Flashing winning color until button press...")

                while not cp.button_a and not cp.button_b:
                    flash_color(winning_color, 1)

                round_colors = []
                cp.pixels.fill((0, 0, 0))
                cp.pixels.show()

    # End of game or waiting to restart
    cp.pixels.fill((255, 0, 0))
    cp.pixels.show()
    time.sleep(5)
    print("Press button A to restart the game.")
    while not cp.button_a:
        time.sleep(0.1)
        cp.pixels.fill((0, 0, 0))
        cp.pixels.show()
        break
