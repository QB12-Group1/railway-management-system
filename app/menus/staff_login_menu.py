from typing import TYPE_CHECKING

from app.menus.base import BaseMenu
from app.models.user import UserRole

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class StaffLoginMenu(BaseMenu):
    """Menu for authenticating staff members."""

    def display(self, controller: MenuController) -> None:
        """Ask for staff credentials and return to the main menu after success."""
        self.show_title("Staff Login")

        username = self.get_required_feedback("Username: ")
        if username is None:
            self.cancel_operation(controller, exit_menu=True)
            return

        password = self.get_required_feedback("Password: ")
        if password is None:
            self.cancel_operation(controller, exit_menu=True)
            return

        result = controller.services.auth.log_in(username, password)
        if not result.success:
            print(result.message)
            return

        if result.data is None or result.data.role != UserRole.STAFF:
            print("Only staff members can access this menu.")
            return

        print(f"Welcome back, {result.data.username}! Staff login successful.")
        controller.pop()
