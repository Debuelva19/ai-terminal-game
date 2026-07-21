import os
import random

# Grid size
GRID_SIZE = 5

# Win condition
WIN_SCORE = 10

# Player starting position (row, col)
player_pos = [0, 0]

# Score tracker
score = 0

# Collectible position (row, col)
collectible_pos = [0, 0]


def spawn_collectible():
    """Place the collectible at a random position that is not the player's."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if [row, col] != player_pos:
            collectible_pos[0] = row
            collectible_pos[1] = col
            break


def draw_grid():
    """Draw the 5x5 grid with the player and collectible on it."""
    # Clear the terminal so each frame is fresh
    os.system("clear" if os.name != "nt" else "cls")

    print("=" * 20)
    print("   TERMINAL GAME")
    print("=" * 20)
    print(f"   Score: {score}/{WIN_SCORE}")
    print()

    # Build each row of the grid
    for row in range(GRID_SIZE):
        line = ""
        for col in range(GRID_SIZE):
            if row == player_pos[0] and col == player_pos[1]:
                line += " P"
            elif row == collectible_pos[0] and col == collectible_pos[1]:
                line += " X"
            else:
                line += " ."
            if col < GRID_SIZE - 1:
                line += " "
        print("  " + line)
        print()


def handle_movement(command):
    """Update player position based on WASD input, with boundary checks."""
    # W = up (row decreases), S = down (row increases)
    # A = left (col decreases), D = right (col increases)
    if command == "w":
        new_row = player_pos[0] - 1
        if new_row >= 0:
            player_pos[0] = new_row
    elif command == "s":
        new_row = player_pos[0] + 1
        if new_row < GRID_SIZE:
            player_pos[0] = new_row
    elif command == "a":
        new_col = player_pos[1] - 1
        if new_col >= 0:
            player_pos[1] = new_col
    elif command == "d":
        new_col = player_pos[1] + 1
        if new_col < GRID_SIZE:
            player_pos[1] = new_col


def check_collectible():
    """Check if the player is on the collectible. If so, score and respawn."""
    global score
    if player_pos[0] == collectible_pos[0] and player_pos[1] == collectible_pos[1]:
        score += 1
        spawn_collectible()
        return True
    return False


def game_loop():
    """Main game loop - keeps running until the player quits or wins."""
    # Spawn the first collectible
    spawn_collectible()

    while True:
        draw_grid()

        # Check for win condition
        if score >= WIN_SCORE:
            print("  You WIN! 🎉 All items collected!\n")
            break

        # Get input from the player
        user_input = input("  Move: ").strip().lower()

        # Check if the player wants to quit
        if user_input == "q":
            print("\n  Thanks for playing! Catch ya later! 👋\n")
            break

        # Handle WASD movement
        if user_input in ("w", "a", "s", "d"):
            handle_movement(user_input)
            check_collectible()


# Run the game when this file is executed
if __name__ == "__main__":
    game_loop()
