from __future__ import annotations

import random
import time
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from django.http import StreamingHttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

if TYPE_CHECKING:
    from django.http import HttpRequest


class GameView(TemplateView):
    template_name = "gol/game.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["grid"] = [[random.choice([True, False]) for _ in range(20)] for _ in range(20)]  # noqa: S311
        return context


game_view = GameView.as_view()


class UpdateView(View):
    async def get(self, request: HttpRequest) -> StreamingHttpResponse:
        return StreamingHttpResponse(self.stream(request), content_type="text/event-stream")

    @classmethod
    def stream(cls, request: HttpRequest) -> Iterable:
        while True:
            grid = [[random.choice([True, False]) for _ in range(20)] for _ in range(20)]  # noqa: S311
            rendered_grid = render_to_string("gol/game.html#grid", {"grid": grid}, request)
            yield f"data: {rendered_grid.replace('\n', '')}"
            yield "\n\n"
            time.sleep(1)


update_view = UpdateView.as_view()
