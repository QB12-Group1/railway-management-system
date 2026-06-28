from app.menu_controller import MenuController
from app.menus.base import BaseMenu
from app.menus.ticket_purchase_menu import TicketPurchaseMenu
from app.models.user import Customer


class CustomerOperationsMenu(BaseMenu):
    def __init__(self, customer: Customer) -> None:
        self._customer = customer

    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Customer Dashboard",
            {
                "Manage Tickets": lambda controller: controller.push(
                    TicketPurchaseMenu(self._customer)
                ),
                "Manage Wallet": self.show_not_implemented,
                "Update Profile": self.modify_customer,
                "View Profile": self.view_profile,
                "Exit": lambda controller: controller.pop(),
            },
        )

    def view_profile(self, _: MenuController) -> None:
        self.show_title(
            f"Info {self._customer.__class__.__name__}[{self._customer.username}]"
        )
        print(f"Full Name: {self._customer.full_name}")
        print(f"Email: {self._customer.email}")
        print(f"Password: {self._customer.password}")
        self.pause()

    def modify_customer(self, controller: MenuController) -> None:
        self.show_title(f"Update {self._customer}")
        print("Leave blank to Keep current value.")

        full_name = self.get_feedback("New full name: ") or None
        if full_name is not None and self.is_cancel_command(full_name):
            self.cancel_operation(controller)
            return

        email = self.get_feedback("New email: ") or None
        if email is not None and self.is_cancel_command(email):
            self.cancel_operation(controller)
            return

        password = self.get_feedback("New password: ") or None
        if password is not None and self.is_cancel_command(password):
            self.cancel_operation(controller)
            return

        result = controller.services.customer.update_profile(
            self._customer.username, full_name, email, password
        )
        print(result.message)
        self.pause()
