from __future__ import annotations

import time
from collections.abc import Iterable
from typing import TYPE_CHECKING

from django.http import StreamingHttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from .game import Game, Grid

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

ROWS = 40
COLUMNS = 40
UPDATE_INTERVAL = 0.3


class GameView(TemplateView):
    """View for rendering the game template with an initial grid."""

    template_name = "game.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        context["grid"] = Grid(rows=ROWS, columns=COLUMNS)
        context["updatable_cells"] = True
        context["game"] = None
        return self.render_to_response(context)


game_view = GameView.as_view()


class StartGameView(TemplateView):
    """View for starting the game and rendering the control panel template."""

    template_name = "game.html#sse_listener"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        # Passes the params containing the alive cells to create a link for UpdateView SSE connection
        context["update_url"] = reverse("update") + f"?{request.META['QUERY_STRING']}"
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
        while True:
            time.sleep(UPDATE_INTERVAL)
            rendered_grid = render_to_string("game.html#game", {"grid": game.grid, "game": game}, request)
            yield "event: update\n"
            yield f"data: {rendered_grid.replace('\n', '')}"
            yield "\n\n"
            if game.has_ended:
                break
            game.update()

        rendered_grid = render_to_string("game.html#empty_sse_listener", {"grid": game.grid}, request)
        yield "event: end\n"
        yield f"data: {rendered_grid.replace('\n', '')}"
        yield "\n\n"


update_view = UpdateView.as_view()
