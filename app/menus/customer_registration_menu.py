from __future__ import annotations

from typing import TYPE_CHECKING

from app.menus.base import BaseMenu

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class CustomerRegistrationMenu(BaseMenu):
    """Menu for registering a new user account."""

    def display(self, controller: MenuController) -> None:
        self.show_title("Register")

        username = self.get_required_feedback("Username: ")
        if username is None:
            self.cancel_operation(controller, exit_menu=True)
            return

        password = self.get_required_feedback("Password: ")
        if password is None:
            self.cancel_operation(controller, exit_menu=True)
            return

        full_name = self.get_required_feedback("Full name: ")
        if full_name is None:
            self.cancel_operation(controller, exit_menu=True)
            return

        email = self.get_required_feedback("Email: ")
        if email is None:
            self.cancel_operation(controller, exit_menu=True)
            return

        result = controller.services.auth.register_customer(
            username, password, full_name, email
        )

        print(result.message)
        self.pause()
        controller.pop()
        # TODO: push the customer dashboard here
