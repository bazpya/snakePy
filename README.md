# Snake

The classic Snake game in Python, played either by you with the arrow keys or by a small neural network that teaches itself through reinforcement learning (DQN).

## Quick start

Requirements: Python 3.11 with tkinter. The repo includes a devcontainer that sets this up.

```bash
pip install -r requirements.txt   # CPU-only PyTorch, pytest

python play_human.py   # play yourself
python train_ml.py     # train the AI (headless); saves models/brain.pt
python play_ml.py      # watch the trained AI play
```

In VS Code, the same commands are in the Run menu: **Play-Human**, **Play-ML** and **Train-ML**.

## How to play

- The arrow keys steer the snake. Quick presses are queued, one per step.
- Eat the food to grow.
- The game ends when the snake:
  - **crashes** into a wall or itself,
  - **starves**, going too long without food (AI games only), or
  - **wins** by filling the whole grid.

## How the AI learns

Each step:

1. The **Eye** turns the game into 15 numbers, all relative to the snake's heading:
   - danger in five directions
   - where the food and the tail are
   - how much room each turn leaves
   - whether each turn can still reach the tail
2. The **Brain**, a small neural network, estimates how good each turn is: left, ahead or right.
3. The snake takes the best turn. During training, it sometimes takes a random one instead, to explore.

Training is a loop: each step is stored as an experience, with a reward of +1 for food and −1 for crashing or starving. The **Teacher** replays random batches of these experiences to improve the Brain's estimates.

## Project layout

| Path | What it holds |
|---|---|
| `snake/core` | Game rules (`World`), the game driver (`Game`), and the shared types |
| `snake/ui` | Drawing the game in a tkinter window, and pacing it |
| `snake/human` | The human player and keyboard input |
| `snake/ml` | The AI: Eye, Brain, Teacher, replay memory, rewards |
| `play_human.py`, `play_ml.py`, `train_ml.py` | Entry points that wire the parts together |
| `v0/` | The original version, kept for reference |

## Running tests

```bash
pytest
```

Tests sit next to the code they test (`world.py` → `world_test.py`). VS Code has **Test-All** plus one config per package.

## Design notes

- **Test first:** every change starts with a failing test.
- **Contracts:** each `XConcept` is a small `Protocol` defined by the class that uses it, holding only what that class needs.
- **Naming:**
  - Method names are verbs.
  - Calls read as plain English.
  - An implementation's qualifier goes at the end of its name (`CanvasTk`), so its file sorts next to its contract's file.
- **One-way flow:** `World` → `WorldState` → players and observers → turn → `World`.

