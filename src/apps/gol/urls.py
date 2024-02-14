from django.urls import path

from .views import game_view, start_game_view, update_view

urlpatterns = [
    path("", game_view, name="game"),
    path("start-game", start_game_view, name="start-game"),
    path("update/", update_view, name="update"),
]
