from __future__ import annotations

from typing import TYPE_CHECKING

from app.menus.base import BaseMenu

"""Example main menu implementation."""


if TYPE_CHECKING:
    from app.menu_controller import MenuController


class MainMenu(BaseMenu):
    """Primary application menu."""

    def display(self, controller: MenuController) -> None:
        self.show_title("Main Menu")
        self.show_options(
            ["Enter as 'Admin'", "Enter as 'Staff'", "Enter as 'Customer'", "Exit"]
        )
        choice = self.get_feedback()
        match choice:
            case "1":
                pass  # TODO: call admin menu
            case "2":
                pass  # TODO: call staff menu
            case "3":
                pass  # TODO: call user menu
            case "4":
                print("Exiting...")
                controller.pop()
            case _:
                self.invalid_input()
