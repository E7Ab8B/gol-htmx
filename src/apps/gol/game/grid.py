from __future__ import annotations

from collections.abc import Iterator
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from .cell import Cell

if TYPE_CHECKING:
    from ._types import AliveCells, CellGrid


@dataclass(slots=True, kw_only=True)
class Grid:
    """Represents a grid of cells in a cellular automaton.

    Args:
        rows: The number of rows in the grid.
        columns: The number of columns in the grid.
        init_cell_grid: Initial state of the cell grid.
            If `None`, an empty cell grid will be created.

    Attributes:
        cell_grid: The 2D grid of cells.

    Examples:
        >>> grid = Grid(rows=3, columns=3)
        >>> bool(grid.cell_grid[0][0])
        False

        >>> fresh_grid = grid.fresh_cell_grid()
        >>> len(fresh_grid)
        3

        >>> grid.set_cell(1, 1, True)
        >>> grid.alive_neighbors(1, 0)
        0
    """

    rows: int
    columns: int
    init_cell_grid: InitVar[CellGrid | None] = None
    cell_grid: CellGrid = field(init=False)

    def __post_init__(self, init_cell_grid: CellGrid | None) -> None:
        self.cell_grid = self._empty_cell_grid() if init_cell_grid is None else init_cell_grid

    def __len__(self) -> int:
        """Returns the total number of cells in the grid."""
        return self.rows * self.columns

    def __iter__(self) -> Iterator[tuple[int, int, Cell]]:
        """Yields (row, column, cell) tuples for each cell in the grid."""
        for row in range(self.rows):
            for col in range(self.columns):
                yield row, col, self.cell_grid[row][col]

    @property
    def cols(self) -> int:
        """Returns the number of columns in the grid (alias for :attr:`columns`)."""
        return self.columns

    @classmethod
    def generate_grid(cls, *, rows: int, columns: int, alive_cells: AliveCells) -> Grid:
        """Generate a grid with specified dimensions and initial alive cells."""
        cell_grid = []
        for row in range(rows):
            alive_columns = alive_cells.get(str(row))
            cell_grid.append([Cell(col in alive_columns) if alive_columns else Cell() for col in range(columns)])

        return Grid(rows=rows, columns=columns, init_cell_grid=cell_grid)

    def _empty_cell_grid(self) -> CellGrid:
        """Returns an empty cell grid with all cells in the dead state."""
        return [[Cell() for _ in range(self.columns)] for _ in range(self.rows)]

    def set_cell(self, row: int, col: int, value: bool) -> None:
        """Sets the state of a cell in the grid."""
        self.cell_grid[row][col].is_alive = value

    def _is_cell_in_bounds(self, row: int, col: int) -> bool:
        """Checks if a given cell coordinates are within the grid bounds."""
        return 0 <= row < self.rows and 0 <= col < self.columns

    def alive_neighbors(self, row: int, col: int) -> int:
        """Counts the number of alive neighbors for a given cell."""
        # fmt: off
        neighbor_offsets: list[tuple[int, int]] = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        # fmt: on

        neighbors_state: list[bool] = []
        for neighbor_row_offset, neighbor_col_offset in neighbor_offsets:
            neighbor_row, neighbor_col = row + neighbor_row_offset, col + neighbor_col_offset

            if self._is_cell_in_bounds(neighbor_row, neighbor_col):
                neighbors_state.append(self.cell_grid[neighbor_row][neighbor_col].is_alive)
            else:
                neighbors_state.append(False)
        return sum(neighbors_state)
