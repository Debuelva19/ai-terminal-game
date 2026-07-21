import os

# Grid size
GRID_SIZE = 5

# Player starting position (row, col)
player_pos = [0, 0]


def draw_grid():
    """Draw the 5x5 grid with the player on it."""
    # Clear the terminal so each frame is fresh
    os.system("clear" if os.name != "nt" else "cls")

    print("=" * 20)
    print("   TERMINAL GAME")
    print("=" * 20)
    print()

    # Build each row of the grid
    for row in range(GRID_SIZE):
        line = ""
        for col in range(GRID_SIZE):
            if row == player_pos[0] and col == player_pos[1]:
                line += " P"
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


def game_loop():
    """Main game loop - keeps running until the player quits."""
    while True:
        draw_grid()

        # Get input from the player
        user_input = input("  Move: ").strip().lower()

        # Check if the player wants to quit
        if user_input == "q":
            print("\n  Thanks for playing! Catch ya later! 👋\n")
            break

        # Handle WASD movement
        if user_input in ("w", "a", "s", "d"):
            handle_movement(user_input)


# Run the game when this file is executed
if __name__ == "__main__":
    game_loop()
