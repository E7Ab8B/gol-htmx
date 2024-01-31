from __future__ import annotations

from apps.gol.game.cell import Cell


def test_cell_default_state() -> None:
    cell = Cell()

    assert not bool(cell)


def test_cell_birth() -> None:
    cell = Cell()
    cell.birth()

    assert bool(cell)


def test_cell_death() -> None:
    cell = Cell(is_alive=True)
    cell.death()

    assert not bool(cell)


def test_cell_equality() -> None:
    cell1 = Cell(is_alive=True)
    cell2 = Cell(is_alive=True)

    assert cell1 == cell2


def test_cell_inequality() -> None:
    cell1 = Cell(is_alive=True)
    cell2 = Cell(is_alive=False)

    assert cell1 != cell2
