"""Conway's Game of Life Rules

This module defines rules for Conway's Game of Life, a cellular automaton.
The rules determine the state of a cell in the next generation based on its
current state and the number of alive neighbors.

Rules:
1. Underpopulation: A live cell with fewer than 2 live neighbors dies.
2. Survival: A live cell with 2 or 3 live neighbors survives.
3. Overpopulation: A live cell with more than 3 live neighbors dies.
4. Reproduction: A dead cell with exactly 3 live neighbors becomes alive.

Rule Function Explanation:
- A rule function takes a cell and the count of its alive neighbors as arguments.
- It returns a `bool` or `None`.
- If the rule applies to the cell, it may change the cell's state and return
    `True` or `False`.
- If the rule does not apply to the cell, it returns `None`, indicating no
    change to the cell.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .cell import Cell


def underpopulation(cell: Cell, alive_neighbors: int) -> Literal[False] | None:
    """Apply underpopulation rule.

    If the `cell` is alive and has fewer than 2 alive neighbors, it dies.
    """
    if cell.is_alive and alive_neighbors < 2:
        return False
    return None


def survival(cell: Cell, alive_neighbors: int) -> Literal[True] | None:
    """Apply survival rule.

    If the `cell` is alive and has 2 or 3 alive neighbors, it survives.
    """
    if cell.is_alive and alive_neighbors in range(2, 4):
        return True
    return None
