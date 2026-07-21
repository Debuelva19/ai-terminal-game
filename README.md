# Eat Man

A terminal-based Python game where you play as a cowboy collecting eggs while dodging hazards on a 5x5 grid.

> *"Eat the egg, avoid the hazard"*

## Overview

Eat Man is a simple but addictive text-based game built entirely in Python. Navigate a 🤠 across a grid, collect 🥚 to score points, and avoid the ☄️ at all costs. Reach a score of 10 to win — but one wrong step onto a hazard and it's game over.

Built as a learning project to practice Python fundamentals, game loop design, and test-driven development.

## Features

- **WASD Movement** — Classic keyboard controls to navigate the 5x5 grid
- **Boundary Detection** — Player cannot move outside the grid edges
- **Collectible System** — Eggs spawn at random positions; collect them to increase your score
- **Hazard System** — A comet spawns at a random position; step on it and the game ends
- **Score Tracking** — Live score display each turn, progressing toward the win condition
- **Win/Lose Conditions** — Reach score 10 to win, or hit a hazard to lose
- **Play Again** — After each round, choose to restart or exit cleanly
- **Intro Screen** — Game name, story, and emoji legend displayed at startup
- **Custom Theme** — Fully themed with unique emojis and messages

## How to Run

### Prerequisites

- Python 3.7 or higher
- `pytest` (for running tests)

### Play the Game

```bash
python game.py
```

### Run the Tests

```bash
pytest test_game.py -v
```

This runs all 57 automated tests covering movement, boundaries, spawning, scoring, hazards, display, and more.

## Project Structure

```
ai-terminal-game/
├── game.py          # Main game logic and loop
├── test_game.py     # Pytest test suite (57 tests)
├── .gitignore       # Ignores __pycache__, .pytest_cache, .opencode
└── README.md        # This file
```

## What I Learned

### Iterative Development

This game was built step by step, not all at once. Each feature was added one at a time — first the grid, then movement, then collectibles, hazards, win/lose conditions, restart, and finally theming. This incremental approach made it easy to understand each piece of the system before building on top of it.

### Engineering Prompts to Prevent Regression

Each time a new feature was added, the existing tests were updated and expanded to cover the new behaviour. This meant that when something broke (and it did), the tests caught it immediately. Writing clear, specific prompts for each change — rather than trying to do everything at once — kept the codebase stable throughout development.

### Automated Testing with Pytest

Writing 57 tests taught me the value of test-driven confidence. Every function in the game has dedicated tests: movement in all directions, boundary checks at every edge, spawn logic that avoids overlaps, and display tests that verify exactly what the player sees. Running `pytest` before every commit became a habit that prevented broken code from ever reaching the repository.

## Controls

| Key | Action |
|-----|--------|
| `W` | Move up |
| `A` | Move left |
| `S` | Move down |
| `D` | Move right |
| `Q` | Quit game |
| `Y` | Play again (after win/lose) |
| `N` | Exit (after win/lose) |

## License

This project was built as a learning exercise with Correlation One.
