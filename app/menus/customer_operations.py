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
            "Staff Dashboard",
            {
                "Manage Tickets": lambda controller: controller.push(
                    TicketPurchaseMenu(self._customer)
                ),
                "Update Profile": self.show_not_implemented,
                "Exit": lambda controller: controller.pop(),
            },
        )
