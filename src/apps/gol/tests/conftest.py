from __future__ import annotations

import pytest

from apps.gol.game.grid import Grid


@pytest.fixture()
def empty_grid() -> Grid:
    return Grid(rows=3, columns=3)


@pytest.fixture()
def glider_grid() -> Grid:
    grid = Grid(rows=10, columns=10)
    grid.set_cell(0, 1, True)
    grid.set_cell(1, 2, True)
    grid.set_cell(2, 0, True)
    grid.set_cell(2, 1, True)
    grid.set_cell(2, 2, True)
    return grid


@pytest.fixture()
def blinker_grid() -> Grid:
    grid = Grid(rows=10, columns=10)
    grid.set_cell(1, 0, True)
    grid.set_cell(1, 1, True)
    grid.set_cell(1, 2, True)
    return grid
