from __future__ import annotations

from django.views.generic import TemplateView


class GameView(TemplateView):
    template_name = "gol/game.html"


game_view = GameView.as_view()
