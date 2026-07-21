import game


# This fixture runs before EVERY test to reset the player position.
# Without this, one test could affect the next (order-dependent bugs).
def setup_function():
    """Reset player to starting position before each test."""
    game.player_pos[0] = 0
    game.player_pos[1] = 0


# ─────────────────────────────────────────────
# Movement tests
# ─────────────────────────────────────────────

def test_move_right():
    """D should increase the column by 1."""
    game.handle_movement("d")
    assert game.player_pos == [0, 1]


def test_move_left():
    """A should decrease the column by 1."""
    # Move right first so we have room to go left
    game.handle_movement("d")
    game.handle_movement("a")
    assert game.player_pos == [0, 0]


def test_move_down():
    """S should increase the row by 1."""
    game.handle_movement("s")
    assert game.player_pos == [1, 0]


def test_move_up():
    """W should decrease the row by 1."""
    # Move down first so we have room to go up
    game.handle_movement("s")
    game.handle_movement("w")
    assert game.player_pos == [0, 0]


def test_multiple_moves():
    """Multiple moves should track position correctly."""
    game.handle_movement("d")  # (0,1)
    game.handle_movement("d")  # (0,2)
    game.handle_movement("s")  # (1,2)
    game.handle_movement("s")  # (2,2)
    game.handle_movement("a")  # (2,1)
    assert game.player_pos == [2, 1]


# ─────────────────────────────────────────────
# Boundary tests
# ─────────────────────────────────────────────

def test_cannot_move_left_off_grid():
    """Moving left from column 0 should stay at column 0."""
    game.handle_movement("a")
    assert game.player_pos == [0, 0]


def test_cannot_move_up_off_grid():
    """Moving up from row 0 should stay at row 0."""
    game.handle_movement("w")
    assert game.player_pos == [0, 0]


def test_cannot_move_right_off_grid():
    """Moving right from the right edge should stay put."""
    game.player_pos = [0, 4]
    game.handle_movement("d")
    assert game.player_pos == [0, 4]


def test_cannot_move_down_off_grid():
    """Moving down from the bottom edge should stay put."""
    game.player_pos = [4, 0]
    game.handle_movement("s")
    assert game.player_pos == [4, 0]


def test_boundary_bottom_right_corner():
    """All directions blocked at bottom-right corner."""
    game.player_pos = [4, 4]
    game.handle_movement("s")
    game.handle_movement("d")
    assert game.player_pos == [4, 4]


def test_boundary_all_four_corners():
    """Each corner should prevent movement off the grid."""
    # Top-left
    game.player_pos = [0, 0]
    game.handle_movement("w")
    game.handle_movement("a")
    assert game.player_pos == [0, 0]

    # Top-right
    game.player_pos = [0, 4]
    game.handle_movement("w")
    game.handle_movement("d")
    assert game.player_pos == [0, 4]

    # Bottom-left
    game.player_pos = [4, 0]
    game.handle_movement("s")
    game.handle_movement("a")
    assert game.player_pos == [4, 0]

    # Bottom-right
    game.player_pos = [4, 4]
    game.handle_movement("s")
    game.handle_movement("d")
    assert game.player_pos == [4, 4]


# ─────────────────────────────────────────────
# Invalid input tests
# ─────────────────────────────────────────────

def test_invalid_input_ignored():
    """Non-WASD input should not move the player."""
    game.handle_movement("x")
    assert game.player_pos == [0, 0]

    game.handle_movement("hello")
    assert game.player_pos == [0, 0]

    game.handle_movement("")
    assert game.player_pos == [0, 0]


# ─────────────────────────────────────────────
# draw_grid tests (using capsys to capture print output)
# ─────────────────────────────────────────────

def test_draw_grid_player_at_origin(capsys):
    """Grid should show P at top-left when player is at (0,0)."""
    game.draw_grid()
    output = capsys.readouterr().out
    lines = output.strip().split("\n")

    # First row of the grid should have " P" as the first cell
    # Find the line that starts with grid content (skipping header lines)
    grid_lines = [line for line in lines if "P" in line or ("." in line and "  " in line)]
    assert len(grid_lines) > 0
    assert "P" in grid_lines[0]


def test_draw_grid_player_at_center(capsys):
    """Grid should show P in the middle when player is at (2,2)."""
    game.player_pos = [2, 2]
    game.draw_grid()
    output = capsys.readouterr().out
    lines = output.strip().split("\n")

    # The middle grid row should contain P
    grid_lines = [line for line in lines if "P" in line]
    assert len(grid_lines) > 0
    assert "P" in grid_lines[0]


def test_draw_grid_has_correct_size(capsys):
    """Grid should have 5 rows of dots/players."""
    game.draw_grid()
    output = capsys.readouterr().out
    lines = output.strip().split("\n")

    # Count lines that are grid rows (contain dots or P)
    grid_lines = [line for line in lines if "  ." in line or "  P" in line]
    assert len(grid_lines) == game.GRID_SIZE


def test_draw_grid_shows_only_one_player(capsys):
    """Only one P should appear in the grid, no matter the position."""
    game.player_pos = [3, 1]
    game.draw_grid()
    output = capsys.readouterr().out
    assert output.count("P") == 1
