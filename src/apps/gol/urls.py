from django.urls import path

from .views import game_view, update_view

urlpatterns = [
    path("", game_view, name="game"),
    path("update/", update_view, name="update"),
]
