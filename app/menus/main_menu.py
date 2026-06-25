from __future__ import annotations

from typing import TYPE_CHECKING

from app.menus.admin_login_menu import AdminLoginMenu
from app.menus.base import BaseMenu

"""Example main menu implementation."""


if TYPE_CHECKING:
    from app.menu_controller import MenuController


class MainMenu(BaseMenu):
    """Primary application menu."""

    def display(self, controller: MenuController) -> None:
        """Render the application entry menu and route to the selected section."""
        self.handle_options(
            controller,
            "Main Menu",
            {
                "Enter as 'Admin'": lambda controller: controller.push(
                    AdminLoginMenu()
                ),
                "Enter as 'Staff'": lambda controller: print(
                    "Staff menu is not implemented yet."
                ),
                "Enter as 'Customer'": lambda controller: print(
                    "Customer menu is not implemented yet."
                ),
                "Exit": self.exit,
            },
        )

    def exit(self, controller: MenuController) -> None:
        """Close the main menu and stop the controller loop."""
        print("Exiting...")
        controller.pop()
