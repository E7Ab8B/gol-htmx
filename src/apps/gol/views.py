from __future__ import annotations

import contextlib
import time
from collections.abc import Iterable
from typing import TYPE_CHECKING

from django.http import StreamingHttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from .forms import CellUpdateForm
from .game import Cell, Game, Grid

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from .game._types import AliveCells


def generate_grid(request: HttpRequest) -> Grid:
    """Generate a grid based on session data or initialize an empty grid."""
    return Grid.generate_grid(rows=50, columns=50, alive_cells=request.session.setdefault("alive_cells", {}))


class GameView(TemplateView):
    """View for rendering the game template with an initial grid."""

    template_name = "game.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        context["grid"] = generate_grid(request)
        context["updatable_cells"] = True
        return self.render_to_response(context)


game_view = GameView.as_view()


class StartGameView(TemplateView):
    template_name = "game.html#playing_control_panel"


start_game_view = StartGameView.as_view()


class UpdateView(View):
    """View for streaming real-time updates of the game grid."""

    def get(self, request: HttpRequest) -> StreamingHttpResponse:
        return StreamingHttpResponse(self.stream(request), content_type="text/event-stream")

    @staticmethod
    def stream(request: HttpRequest) -> Iterable:
        """Generate a continuous stream of game grid updates."""
        game = Game(generate_grid(request))
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
        row = form.cleaned_data["row"]
        col = form.cleaned_data["col"]

        alive_cells: AliveCells = request.session.setdefault("alive_cells", {})
        alive_columns = alive_cells.setdefault(str(row), [])

        if cell.is_alive:
            alive_columns.append(col)
        else:
            # It shouldn't be technically possible to have a missing column, but left it as a safeguard
            with contextlib.suppress(ValueError):
                alive_columns.remove(col)

        # Mark the session as modified to ensure changes to alive_cells, especially nested structures like alive_columns
        # are saved. Django's default mechanism might not catch modifications within nested structures.
        # https://docs.djangoproject.com/en/dev/topics/http/sessions/#when-sessions-are-saved
        request.session.modified = True

        return self.render_to_response({"col": row, "row": col, "cell": cell, "updatable_cells": True})


cell_update_view = CellUpdateView.as_view()
