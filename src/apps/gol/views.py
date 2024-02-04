from __future__ import annotations

import time
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from django.http import StreamingHttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from .game import Game, Grid

if TYPE_CHECKING:
    from django.http import HttpRequest


def init_grid() -> Grid:
    grid = Grid(rows=50, columns=50)
    grid.set_cell(0, 0, True)
    grid.set_cell(1, 3, True)
    grid.set_cell(2, 1, True)
    grid.set_cell(2, 2, True)
    grid.set_cell(2, 3, True)
    return grid


class GameView(TemplateView):
    """View for rendering the game template with an initial grid."""

    template_name = "game.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["grid"] = init_grid()
        return context


game_view = GameView.as_view()


class UpdateView(View):
    """View for streaming real-time updates of the game grid."""

    async def get(self, request: HttpRequest) -> StreamingHttpResponse:
        return StreamingHttpResponse(self.stream(request), content_type="text/event-stream")

    @classmethod
    def stream(cls, request: HttpRequest) -> Iterable:
        """Generate a continuous stream of game grid updates."""
        game = Game(init_grid())
        while True:
            rendered_grid = render_to_string("game.html#grid", {"grid": game.grid}, request)
            yield f"data: {rendered_grid.replace('\n', '')}"
            yield "\n\n"
            game.update()
            time.sleep(0.5)


update_view = UpdateView.as_view()
