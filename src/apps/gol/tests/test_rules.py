from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import pytest

from apps.gol.game.cell import Cell
from apps.gol.game.rules import survival, underpopulation

if TYPE_CHECKING:
    type AliveNeighbors = int
    type RuleResult = bool | None

ALIVE_NEIGHBORS_RANGE = range(9)


class TestUnderpopulationRule:
    @staticmethod
    @pytest.mark.parametrize(
        ("alive_neighbors", "expected"),
        [
            (0, False),
            (1, False),
            (2, None),
            (3, None),
            (4, None),
            (5, None),
            (6, None),
            (7, None),
            (8, None),
        ],
    )
    def test_alive_cell(alive_neighbors: int, expected: Literal[False] | None) -> None:
        state = underpopulation(Cell(is_alive=True), alive_neighbors)

        assert state is expected

    @staticmethod
    @pytest.mark.parametrize("alive_neighbors", ALIVE_NEIGHBORS_RANGE)
    def test_dead_cell(alive_neighbors: int) -> None:
        state = underpopulation(Cell(), alive_neighbors)

        assert state is None


class TestSurvivalRule:
    @staticmethod
    @pytest.mark.parametrize(
        ("alive_neighbors", "expected"),
        [
            (0, None),
            (1, None),
            (2, True),
            (3, True),
            (4, None),
            (5, None),
            (6, None),
            (7, None),
            (8, None),
        ],
    )
    def test_alive_cell(alive_neighbors: int, expected: Literal[True] | None) -> None:
        state = survival(Cell(is_alive=True), alive_neighbors)

        assert state is expected

    @staticmethod
    @pytest.mark.parametrize("alive_neighbors", ALIVE_NEIGHBORS_RANGE)
    def test_dead_cell(alive_neighbors: int) -> None:
        state = survival(Cell(), alive_neighbors)

        assert state is None
