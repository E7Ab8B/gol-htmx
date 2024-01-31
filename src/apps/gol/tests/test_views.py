from __future__ import annotations

from typing import TYPE_CHECKING

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client


class TestGameView:
    url = reverse("game")

    def test_view_returns_200(self, client: Client) -> None:
        response = client.get(self.url)

        assert response.status_code == 200

    def test_uses_template(self, client: Client) -> None:
        response = client.get(self.url)

        assertTemplateUsed(response, "game.html")  # pyright: ignore[reportArgumentType]


class TestUpdateView:
    url = reverse("update")

    def test_view_returns_200(self, client: Client) -> None:
        response = client.get(self.url)

        assert response.status_code == 200
