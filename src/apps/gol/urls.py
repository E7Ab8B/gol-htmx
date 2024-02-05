from django.urls import path

from .views import cell_update_view, game_view, update_view

urlpatterns = [
    path("", game_view, name="game"),
    path("update/", update_view, name="update"),
    path("cell-update/", cell_update_view, name="cell-update"),
]
