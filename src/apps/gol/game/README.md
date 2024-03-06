# Game of Life Logic

This directory contains the core logic for the Game of Life implementation in this project.

## Files

- [game.py](game.py): Contains the `Game` class, which represents the state and logic of Conway's Game of Life.
- [grid.py](grid.py): Contains the `Grid` class, which represents the grid of cells for the game.
- [cell.py](cell.py): Contains the `Cell` class, which represents a single cell in the game.
- [rules.py](rules.py): Contains the rules defining the game's evolution.

## Usage

To use the Game of Life logic, create an instance of the `Game` class with an initial `Grid` of `Cell`s. Then, call the `update` method on the `Game` instance to advance the game by one generation.

```python
from apps.gol.game import Game, Grid

# Create a new grid
grid = Grid(rows=20, columns=20)

# Set some cells to be alive
grid.set_cell(1, 0, True)
grid.set_cell(1, 1, True)
grid.set_cell(1, 2, True)

# Create a new game with the grid
game = Game(grid=grid)

# Update the game
game.update()
```
