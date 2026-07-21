import game


# This fixture runs before EVERY test to reset game state.
# Without this, one test could affect the next (order-dependent bugs).
def setup_function():
    """Reset all game state before each test."""
    game.player_pos[0] = 0
    game.player_pos[1] = 0
    game.score = 0
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 0


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
# Collectible spawn tests
# ─────────────────────────────────────────────

def test_spawn_not_on_player():
    """Collectible should never spawn on the player's position."""
    # Run spawn many times with player at (0,0)
    game.player_pos = [0, 0]
    for _ in range(50):
        game.spawn_collectible()
        assert game.collectible_pos != [0, 0]


def test_spawn_not_on_player_any_position():
    """Collectible should never spawn on the player, regardless of where they are."""
    game.player_pos = [2, 2]
    for _ in range(50):
        game.spawn_collectible()
        assert game.collectible_pos != [2, 2]


def test_spawn_within_grid():
    """Collectible should always be within grid bounds."""
    for _ in range(50):
        game.spawn_collectible()
        assert 0 <= game.collectible_pos[0] < game.GRID_SIZE
        assert 0 <= game.collectible_pos[1] < game.GRID_SIZE


# ─────────────────────────────────────────────
# Collectible pickup tests
# ─────────────────────────────────────────────

def test_collectible_pickup_increases_score():
    """Moving onto the collectible should increase score by 1."""
    game.collectible_pos = [0, 1]
    game.handle_movement("d")  # move to (0,1)
    collected = game.check_collectible()
    assert collected is True
    assert game.score == 1


def test_collectible_pickup_respawns():
    """After pickup, the collectible should respawn at a new position."""
    game.collectible_pos = [0, 1]
    game.handle_movement("d")  # move to (0,1)
    game.check_collectible()
    # Collectible should no longer be at (0,1)
    assert game.collectible_pos != [0, 1]


def test_no_pickup_when_not_on_collectible():
    """Moving to an empty square should not score."""
    game.collectible_pos = [3, 3]
    game.handle_movement("d")  # move to (0,1)
    collected = game.check_collectible()
    assert collected is False
    assert game.score == 0


def test_score_starts_at_zero():
    """Score should start at 0."""
    assert game.score == 0


def test_multiple_pickups():
    """Picking up multiple collectibles should increase score each time."""
    for i in range(3):
        # Place collectible right in front of the player
        game.collectible_pos = [0, 1]
        game.handle_movement("d")  # move onto collectible
        game.check_collectible()
        assert game.score == i + 1
        # Move back to (0,0) for next round
        game.handle_movement("a")


# ─────────────────────────────────────────────
# Win condition tests
# ─────────────────────────────────────────────

def test_win_condition_reached():
    """Score should reach WIN_SCORE and trigger a win."""
    game.score = game.WIN_SCORE - 1
    game.collectible_pos = [0, 1]
    game.handle_movement("d")
    game.check_collectible()
    assert game.score == game.WIN_SCORE


def test_win_score_constant():
    """WIN_SCORE should be 10."""
    assert game.WIN_SCORE == 10


# ─────────────────────────────────────────────
# draw_grid tests (using capsys to capture print output)
# ─────────────────────────────────────────────

def test_draw_grid_player_at_origin(capsys):
    """Grid should show P at top-left when player is at (0,0)."""
    game.spawn_collectible()
    game.draw_grid()
    output = capsys.readouterr().out

    # First grid row should contain P
    grid_lines = [line for line in output.split("\n") if "  ." in line or "  P" in line or "  X" in line]
    assert len(grid_lines) > 0
    assert "P" in grid_lines[0]


def test_draw_grid_player_at_center(capsys):
    """Grid should show P in the middle when player is at (2,2)."""
    game.player_pos = [2, 2]
    game.spawn_collectible()
    game.draw_grid()
    output = capsys.readouterr().out

    grid_lines = [line for line in output.split("\n") if "P" in line]
    assert len(grid_lines) > 0
    assert "P" in grid_lines[0]


def test_draw_grid_has_correct_size(capsys):
    """Grid should have 5 rows of dots/players/collectibles."""
    game.spawn_collectible()
    game.draw_grid()
    output = capsys.readouterr().out

    grid_lines = [line for line in output.split("\n") if "  ." in line or "  P" in line or "  X" in line]
    assert len(grid_lines) == game.GRID_SIZE


def test_draw_grid_shows_collectible(capsys):
    """Grid should show X for the collectible."""
    game.collectible_pos = [2, 3]
    game.draw_grid()
    output = capsys.readouterr().out
    assert "X" in output


def test_draw_grid_shows_score(capsys):
    """Grid header should display the current score."""
    game.score = 7
    game.spawn_collectible()
    game.draw_grid()
    output = capsys.readouterr().out
    assert "Score: 7/10" in output


def test_draw_grid_shows_only_one_player(capsys):
    """Only one P should appear in the grid, no matter the position."""
    game.player_pos = [3, 1]
    game.spawn_collectible()
    game.draw_grid()
    output = capsys.readouterr().out
    assert output.count("P") == 1
