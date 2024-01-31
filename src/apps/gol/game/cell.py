from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Cell:
    """Represents a cell in a cellular automaton. The default state is dead.

    Examples:
        >>> cell = Cell()
        >>> bool(cell)
        False

        >>> cell.birth()
        >>> bool(cell)
        True

        >>> cell.death()
        >>> bool(cell)
        False
    """

    is_alive: bool = False

    def __bool__(self) -> bool:
        return self.is_alive

    def birth(self) -> None:
        """Sets the cell's state to alive."""
        self.is_alive = True

    def death(self) -> None:
        """Sets the cell's state to dead."""
        self.is_alive = False
