from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .grid import Grid
from .rules import game_rules

if TYPE_CHECKING:
    from ._types import Rule
    from .cell import Cell


@dataclass(slots=True)
class Game:
    """Represents the state and logic of Conway's Game of Life.

    Args:
        grid: The initial grid of cells for the game.
        rules: The rules defining the game's evolution.
            Defaults to the predefined rules (Conway's Game of Life).

    Examples:
        >>> grid = Grid(rows=20, columns=20)
        >>> grid.set_cell(1, 0, True)
        >>> grid.set_cell(1, 1, True)
        >>> grid.set_cell(1, 2, True)
        >>> game = Game(grid=grid)
        >>> game.update()
    """

    grid: Grid
    rules: tuple[Rule, ...] = field(default=game_rules, repr=False)
    _previous_grid: Grid | None = field(init=False)
    _generation: int = field(init=False)

    def __post_init__(self) -> None:
        self._previous_grid = None
        self._generation = 0

    @property
    def has_ended(self) -> bool:
        """Indicates whether the game has reached a conclusion or termination.

        Compares if the current grid is the same as the previous grid.
        """
        return self.grid == self._previous_grid

    @property
    def generation(self) -> int:
        """The current generation of the game."""
        return self._generation

    def update(self) -> None:
        """Advances the game state by applying rules to each cell.

        Notes:
            The update operation won't advance the game if it has already ended.
        """
        if self.has_ended:
            return

        new_grid = Grid(rows=self.grid.rows, columns=self.grid.cols)
        for row, col, cell in self.grid:
            alive_neighbors = self.grid.alive_neighbors(row, col)
            new_cell_state = self._apply_rules_to_cell(cell, alive_neighbors)
            new_grid.set_cell(row, col, new_cell_state)

        self._previous_grid = self.grid
        self.grid = new_grid
        self._generation += 1

    def _apply_rules_to_cell(self, cell: Cell, alive_neighbors: int) -> bool:
        """Applies the defined rules to a single cell."""
        for rule in self.rules:
            result = rule(cell, alive_neighbors)
            if result is not None:
                return result
        return cell.is_alive
