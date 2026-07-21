import game


# This fixture runs before EVERY test to reset game state.
# Without this, one test could affect the next (order-dependent bugs).
def setup_function():
    """Reset all game state before each test."""
    game.reset_game()


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


def test_spawn_collectible_not_on_hazard():
    """Collectible should never spawn on the hazard's position."""
    game.hazard_pos = [2, 2]
    for _ in range(50):
        game.spawn_collectible()
        assert game.collectible_pos != [2, 2]


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
# Hazard spawn tests
# ─────────────────────────────────────────────

def test_hazard_spawn_not_on_player():
    """Hazard should never spawn on the player's position."""
    game.player_pos = [0, 0]
    for _ in range(50):
        game.spawn_hazard()
        assert game.hazard_pos != [0, 0]


def test_hazard_spawn_not_on_collectible():
    """Hazard should never spawn on the collectible's position."""
    game.collectible_pos = [2, 2]
    for _ in range(50):
        game.spawn_hazard()
        assert game.hazard_pos != [2, 2]


def test_hazard_spawn_within_grid():
    """Hazard should always be within grid bounds."""
    for _ in range(50):
        game.spawn_hazard()
        assert 0 <= game.hazard_pos[0] < game.GRID_SIZE
        assert 0 <= game.hazard_pos[1] < game.GRID_SIZE


# ─────────────────────────────────────────────
# Hazard check tests
# ─────────────────────────────────────────────

def test_hazard_check_returns_true_on_hazard():
    """check_hazard should return True when player is on the hazard."""
    game.hazard_pos = [0, 1]
    game.handle_movement("d")  # move to (0,1)
    assert game.check_hazard() is True


def test_hazard_check_returns_false_when_safe():
    """check_hazard should return False when player is not on the hazard."""
    game.hazard_pos = [3, 3]
    game.handle_movement("d")  # move to (0,1)
    assert game.check_hazard() is False


def test_hazard_does_not_affect_score():
    """Stepping on a hazard should not change the score."""
    game.hazard_pos = [0, 1]
    game.handle_movement("d")
    game.check_hazard()
    assert game.score == 0


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
    game.spawn_hazard()
    game.draw_grid()
    output = capsys.readouterr().out

    # First row of the grid should have "P" as the first cell
    grid_lines = [line for line in output.split("\n") if "  ." in line or "  P" in line or "  C" in line or "  X" in line]
    assert len(grid_lines) > 0
    assert "P" in grid_lines[0]


def test_draw_grid_player_at_center(capsys):
    """Grid should show P in the middle when player is at (2,2)."""
    game.player_pos = [2, 2]
    game.spawn_collectible()
    game.spawn_hazard()
    game.draw_grid()
    output = capsys.readouterr().out

    grid_lines = [line for line in output.split("\n") if "P" in line]
    assert len(grid_lines) > 0
    assert "P" in grid_lines[0]


def test_draw_grid_has_correct_size(capsys):
    """Grid should have 5 rows of dots/players/collectibles/hazards."""
    game.spawn_collectible()
    game.spawn_hazard()
    game.draw_grid()
    output = capsys.readouterr().out

    grid_lines = [line for line in output.split("\n") if "  ." in line or "  P" in line or "  C" in line or "  X" in line]
    assert len(grid_lines) == game.GRID_SIZE


def test_draw_grid_shows_collectible(capsys):
    """Grid should show C for the collectible."""
    game.collectible_pos = [2, 3]
    game.spawn_hazard()
    game.draw_grid()
    output = capsys.readouterr().out
    assert "C" in output


def test_draw_grid_shows_hazard(capsys):
    """Grid should show X for the hazard."""
    game.hazard_pos = [1, 2]
    game.spawn_collectible()
    game.draw_grid()
    output = capsys.readouterr().out
    assert "X" in output


def test_draw_grid_shows_score(capsys):
    """Grid header should display the current score."""
    game.score = 7
    game.spawn_collectible()
    game.spawn_hazard()
    game.draw_grid()
    output = capsys.readouterr().out
    assert "Score: 7/10" in output


def test_draw_grid_shows_only_one_player(capsys):
    """Only one P should appear in the grid, no matter the position."""
    game.player_pos = [3, 1]
    game.spawn_collectible()
    game.spawn_hazard()
    game.draw_grid()
    output = capsys.readouterr().out
    assert output.count("P") == 1


# ─────────────────────────────────────────────
# reset_game tests
# ─────────────────────────────────────────────

def test_reset_game_resets_player():
    """reset_game should move player back to (0,0)."""
    game.player_pos = [3, 4]
    game.reset_game()
    assert game.player_pos == [0, 0]


def test_reset_game_resets_score():
    """reset_game should set score back to 0."""
    game.score = 9
    game.reset_game()
    assert game.score == 0


def test_reset_game_spawns_collectible():
    """reset_game should place the collectible somewhere on the grid."""
    game.reset_game()
    assert 0 <= game.collectible_pos[0] < game.GRID_SIZE
    assert 0 <= game.collectible_pos[1] < game.GRID_SIZE


def test_reset_game_spawns_hazard():
    """reset_game should place the hazard somewhere on the grid."""
    game.reset_game()
    assert 0 <= game.hazard_pos[0] < game.GRID_SIZE
    assert 0 <= game.hazard_pos[1] < game.GRID_SIZE


def test_reset_game_no_overlap():
    """reset_game should ensure player, collectible, and hazard are all separate."""
    # Run reset multiple times to test various random outcomes
    for _ in range(20):
        game.reset_game()
        assert game.player_pos != game.collectible_pos
        assert game.player_pos != game.hazard_pos
        assert game.collectible_pos != game.hazard_pos


# ─────────────────────────────────────────────
# play_again_prompt tests (using monkeypatch to mock input)
# ─────────────────────────────────────────────

def test_play_again_prompt_yes(monkeypatch):
    """Entering 'y' should return True."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert game.play_again_prompt() is True


def test_play_again_prompt_no(monkeypatch):
    """Entering 'n' should return False."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert game.play_again_prompt() is False


def test_play_again_prompt_uppercase(monkeypatch):
    """Entering 'Y' or 'N' (uppercase) should still work."""
    monkeypatch.setattr("builtins.input", lambda _: "Y")
    assert game.play_again_prompt() is True

    monkeypatch.setattr("builtins.input", lambda _: "N")
    assert game.play_again_prompt() is False


def test_play_again_prompt_with_spaces(monkeypatch):
    """Leading/trailing spaces should be handled."""
    monkeypatch.setattr("builtins.input", lambda _: "  y  ")
    assert game.play_again_prompt() is True

    monkeypatch.setattr("builtins.input", lambda _: "  n  ")
    assert game.play_again_prompt() is False


def test_play_again_prompt_invalid_then_valid(monkeypatch):
    """Invalid input should be rejected, then valid input accepted."""
    responses = iter(["hello", "x", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    assert game.play_again_prompt() is True
