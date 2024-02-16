from __future__ import annotations

import time
from collections.abc import Iterable
from typing import TYPE_CHECKING

from django.http import StreamingHttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from .game import Game, Grid

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

ROWS = 40
COLUMNS = 40


class GameView(TemplateView):
    """View for rendering the game template with an initial grid."""

    template_name = "game.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        context["grid"] = Grid(rows=ROWS, columns=COLUMNS)
        context["updatable_cells"] = True
        return self.render_to_response(context)


game_view = GameView.as_view()


class StartGameView(TemplateView):
    """View for starting the game and rendering the control panel template."""

    template_name = "game.html#playing_control_panel"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        # Passes the params containing the alive cells to create a link for UpdateView SSE connection
        context["alive_cells_as_params"] = request.META["QUERY_STRING"]
        return self.render_to_response(context)


start_game_view = StartGameView.as_view()


class UpdateView(View):
    """View for streaming real-time updates of the game grid."""

    def get(self, request: HttpRequest) -> StreamingHttpResponse:
        return StreamingHttpResponse(self.stream(request), content_type="text/event-stream")

    @staticmethod
    def stream(request: HttpRequest) -> Iterable:
        """Generate a continuous stream of game grid updates."""
        # TODO: Validation
        alive_cells = {int(row): [int(col) for col in cols] for row, cols in request.GET.lists()}
        game = Game(Grid.generate_grid(rows=40, columns=40, alive_cells=alive_cells))
        while not game.has_ended:
            time.sleep(0.5)
            rendered_grid = render_to_string("game.html#grid", {"grid": game.grid}, request)
            yield "event: update\n"
            yield f"data: {rendered_grid.replace('\n', '')}"
            yield "\n\n"
            game.update()
        rendered_grid = render_to_string("game.html#fresh_control_panel", {"grid": game.grid}, request)
        yield "event: end\n"
        yield f"data: {rendered_grid.replace('\n', '')}"
        yield "\n\n"


update_view = UpdateView.as_view()
