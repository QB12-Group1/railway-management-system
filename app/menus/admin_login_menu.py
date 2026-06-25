from typing import TYPE_CHECKING

from app.menus.base import BaseMenu
from app.models.user import UserRole

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class AdminLoginMenu(BaseMenu):
    """Menu for authenticating administrators."""

    def display(self, controller: MenuController) -> None:
        """Ask for admin credentials and return to the main menu after success."""
        self.show_title("Admin Login")

        username = self.get_required_feedback("Username: ")
        if username is None:
            self.cancel_operation(controller)
            return

        password = self.get_required_feedback("Password: ")
        if password is None:
            self.cancel_operation(controller)
            return

        result = controller.services.auth.log_in(username, password)
        if not result.success:
            print(result.message)
            return

        if result.data is None or result.data.role != UserRole.ADMIN:
            print("Only admins can access this menu.")
            return

        print(f"Welcome back, {result.data.username}! Admin login successful.")
        self.show_not_implemented(controller)  # TODO: implement admin dashboard menu
        controller.pop()
