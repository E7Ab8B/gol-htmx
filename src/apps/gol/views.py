from __future__ import annotations

import time
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from django.http import StreamingHttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from .forms import CellUpdateForm
from .game import Cell, Game, Grid

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class GameView(TemplateView):
    """View for rendering the game template with an initial grid."""

    template_name = "game.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["grid"] = Grid(rows=50, columns=50)
        context["updatable_cells"] = True
        return context


game_view = GameView.as_view()


class UpdateView(View):
    """View for streaming real-time updates of the game grid."""

    def get(self, request: HttpRequest) -> StreamingHttpResponse:
        return StreamingHttpResponse(self.stream(request), content_type="text/event-stream")

    @classmethod
    def stream(cls, request: HttpRequest) -> Iterable:
        """Generate a continuous stream of game grid updates."""
        game = Game(Grid(rows=50, columns=50))
        while True:
            rendered_grid = render_to_string("game.html#grid", {"grid": game.grid}, request)
            yield f"data: {rendered_grid.replace('\n', '')}"
            yield "\n\n"
            game.update()
            time.sleep(0.5)


update_view = UpdateView.as_view()


class CellUpdateView(TemplateView):
    """View for handling updates to individual cells in the game grid."""

    template_name = "game.html#cell"

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CellUpdateForm(request.POST)
        # TODO: Inform about error
        form.full_clean()
        cell = Cell(is_alive=not form.cleaned_data["is_alive"])

        return self.render_to_response(
            {
                "col": form.cleaned_data["row"],
                "row": form.cleaned_data["col"],
                "cell": cell,
                "updatable_cells": True,
            }
        )


cell_update_view = CellUpdateView.as_view()
