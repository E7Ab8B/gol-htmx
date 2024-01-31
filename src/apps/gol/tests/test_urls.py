from __future__ import annotations

from django.urls import resolve, reverse

from apps.gol.views import GameView, UpdateView


class TestGameUrl:
    expected_url = "/"

    def test_reverse_url_matches_expected(self) -> None:
        url = reverse("game")

        assert url == self.expected_url

    def test_resolves_to_correct_view(self) -> None:
        resolver = resolve(self.expected_url)

        assert resolver.func.view_class == GameView  # pyright: ignore[reportFunctionMemberAccess]


class TestUpdateUrl:
    expected_url = "/update/"

    def test_reverse_url_matches_expected(self) -> None:
        url = reverse("update")

        assert url == self.expected_url

    def test_resolves_to_correct_view(self) -> None:
        resolver = resolve(self.expected_url)

        assert resolver.func.view_class == UpdateView  # pyright: ignore[reportFunctionMemberAccess]
