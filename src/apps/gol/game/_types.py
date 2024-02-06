from __future__ import annotations

from collections.abc import Callable

from .cell import Cell

type Row = list[Cell]

type CellGrid = list[Row]

type Rule = Callable[[Cell, int], bool | None]

type AliveCells = dict[str, list[int]]  # {row: [col, ...]}
