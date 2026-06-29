from typing import TYPE_CHECKING

from app.menus.base import BaseMenu
from app.menus.customer_operations import CustomerOperationsMenu
from app.models.user import Customer

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class CustomerLoginMenu(BaseMenu):
    """Menu for authenticating customers."""

    def display(self, controller: MenuController) -> None:
        """Ask for customer credentials and return to the main menu after success."""
        self.show_title("Customer Login")

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

        print(f"Welcome back, {result.data.username}! Customer login successful.")
        controller.pop()

        if result.data is None or not isinstance(result.data, Customer):
            print("Only customers can access this menu.")
            return
        controller.push(CustomerOperationsMenu(result.data))
