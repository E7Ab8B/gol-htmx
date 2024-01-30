from __future__ import annotations

import random
from typing import Any

from django.views.generic import TemplateView


class GameView(TemplateView):
    template_name = "gol/game.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["grid"] = [[random.choice([True, False]) for _ in range(20)] for _ in range(20)]  # noqa: S311
        return context


game_view = GameView.as_view()
