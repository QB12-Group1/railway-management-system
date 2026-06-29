from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING

from app.menus.admin_login_menu import AdminLoginMenu
from app.menus.base import BaseMenu
from app.menus.customer_auth_menu import CustomerAuthMenu
from app.menus.staff_login_menu import StaffLoginMenu

"""Example main menu implementation."""


if TYPE_CHECKING:
    from app.menu_controller import MenuController


class MainMenu(BaseMenu):
    """Primary application menu."""

    def display(self, controller: MenuController) -> None:
        """Render the application entry menu and route to the selected section."""
        controller.services.auth.register_staff(
            "staff", "1234", "test-staff", "staff@gmail.com"
        )
        controller.services.staff.add_railway(
            "railway", "origin", "destination", ["s1", "s2", "s3"]
        )
        controller.services.staff.add_train(
            "train-1", "railway", 120, 5, 9, 500, 10, 20, time(hour=8)
        )
        self.handle_options(
            controller,
            "Main Menu",
            {
                "Enter as 'Admin'": lambda controller: controller.push(
                    AdminLoginMenu()
                ),
                "Enter as 'Staff'": lambda controller: controller.push(
                    StaffLoginMenu()
                ),
                "Enter as 'Customer'": lambda controller: controller.push(
                    CustomerAuthMenu()
                ),
                "Exit": self.exit,
            },
        )

    def exit(self, controller: MenuController) -> None:
        """Close the main menu and stop the controller loop."""
        print("Exiting...")
        controller.pop()
