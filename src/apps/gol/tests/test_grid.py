from __future__ import annotations

from apps.gol.game.grid import Cell, Grid


def test_default_state_of_cells(empty_grid: Grid) -> None:
    cells = [cell for _, _, cell in empty_grid]

    assert not all(cells)


def test_cells_instance(empty_grid: Grid) -> None:
    instances = [isinstance(cell, Cell) for _, _, cell in empty_grid]

    assert all(instances)


def test_len(empty_grid: Grid) -> None:
    assert len(empty_grid) == 9


def test_iter_structure(empty_grid: Grid) -> None:
    assert all(isinstance(entry, tuple) and len(entry) == 3 for entry in empty_grid)


def test_cols(empty_grid: Grid) -> None:
    assert empty_grid.cols == empty_grid.columns


def test_set_cell(empty_grid: Grid) -> None:
    empty_grid.set_cell(1, 1, True)
    assert empty_grid.cell_grid[1][1].is_alive


def test_is_cell_in_bounds(empty_grid: Grid) -> None:
    assert empty_grid._is_cell_in_bounds(1, 1)
    assert not empty_grid._is_cell_in_bounds(3, 3)


def test_alive_neighbors(empty_grid: Grid) -> None:
    empty_grid.set_cell(1, 0, True)
    empty_grid.set_cell(1, 1, True)

    assert empty_grid.alive_neighbors(0, 0) == 2


def test_custom_initialized_grid() -> None:
    init_cell_grid = [[Cell(True), Cell(True)], [Cell(), Cell()]]
    grid = Grid(rows=2, columns=2, init_cell_grid=init_cell_grid)

    assert grid.cell_grid == init_cell_grid
