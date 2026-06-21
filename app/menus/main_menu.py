from __future__ import annotations

from typing import TYPE_CHECKING

from app.menus.base import BaseMenu

"""Example main menu implementation."""


if TYPE_CHECKING:
    from app.menu_controller import MenuController


class MainMenu(BaseMenu):
    """Primary application menu."""

    def display(self, controller: MenuController) -> None:
        raise NotImplementedError()  # TODO: Create the main menu
