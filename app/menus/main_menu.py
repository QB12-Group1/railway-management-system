from __future__ import annotations

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
        self.ensure_admin_existence(controller)
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

    def ensure_admin_existence(self, controller: MenuController) -> None:
        """
        Ensure that at least one Admin account exists in the system.

        This method checks whether any Admin users are currently registered.
        If no admins exist, it prompts the user to create one by entering a
        username and password. The operation can be cancelled during input.

        Args:
            controller (MenuController): The menu controller providing access
            to application services such as authentication.

        Behavior:
            - Retrieves all admins from the authentication service.
            - If none exist, informs the user that an initial admin account must be created.
            - Prompts the user for an admin username and password.
            - Attempts to register the admin through the auth service.
            - Displays the result message and pauses the interface.
        """
        admins = controller.services.auth.get_all_admins()

        if admins.success and admins.data:
            return

        print("No administrator accounts found.")
        self.pause("You must create an administrator account to continue.")

        while True:
            self.show_title("Admin Registration")

            username = self.get_required_feedback("Enter admin username: ")
            if username is None:
                self.cancel_operation(controller)
                continue

            password = self.get_required_feedback("Enter admin password: ")
            if password is None:
                self.cancel_operation(controller)
                continue

            result = controller.services.auth.register_admin(username, password)
            print(result.message)
            self.pause()

            if result.success:
                break

    def exit(self, controller: MenuController) -> None:
        """Close the main menu and stop the controller loop."""
        print("Exiting...")
        controller.pop()
