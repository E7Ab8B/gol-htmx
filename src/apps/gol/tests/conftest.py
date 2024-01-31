from __future__ import annotations

import pytest

from apps.gol.game.grid import Grid


@pytest.fixture()
def empty_grid() -> Grid:
    return Grid(rows=3, columns=3)
