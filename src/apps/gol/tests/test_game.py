from __future__ import annotations

from apps.gol.game.cell import Cell
from apps.gol.game.game import Game
from apps.gol.game.grid import Grid


def test_initialization(empty_grid: Grid) -> None:
    game = Game(grid=empty_grid)

    assert game.grid == empty_grid
    assert game._previous_grid is None


def test_has_ended_true(empty_grid: Grid) -> None:
    game = Game(grid=empty_grid)
    game._previous_grid = empty_grid

    assert game.has_ended


def test_has_ended_false(empty_grid: Grid, glider_grid: Grid) -> None:
    game = Game(grid=empty_grid)
    game._previous_grid = glider_grid

    assert not game.has_ended


def test_update_updates_previous_state_of_grid(glider_grid: Grid) -> None:
    game = Game(grid=glider_grid)
    game.update()

    assert game.grid != glider_grid
    assert game._previous_grid == glider_grid


def test_update_does_not_advance_after_ending(empty_grid: Grid) -> None:
    # Set up an empty grid with one alive cell
    grid = empty_grid
    grid.set_cell(0, 0, True)

    game = Game(grid=grid)
    game.update()
    # Empty grid after this update
    game.update()
    previous_grid = game.grid

    game.update()

    assert game.grid == previous_grid


def test_apply_rules_to_cell(empty_grid: Grid) -> None:
    game = Game(empty_grid, rules=(lambda cell, alive_neighbors: True,))
    result = game._apply_rules_to_cell(Cell(), 0)

    assert result is True
