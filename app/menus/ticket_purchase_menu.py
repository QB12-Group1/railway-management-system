from typing import TYPE_CHECKING

from app.menus.base import BaseMenu
from app.models.user import Customer

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class TicketPurchaseMenu(BaseMenu):
    def __init__(self, customer: Customer) -> None:
        self._customer = customer

    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Ticket Purchase Menu",
            {
                "Buy Ticket": self.buy_ticket,
                "View Tickets": self.list_tickets,
                "Exit": lambda controller: controller.pop(),
            },
        )

    def buy_ticket(self, controller: MenuController) -> None:
        self.show_title("Available Trains")

        result = controller.services.ticket.get_available_trains()

        if not result.success or not result.data:
            print(result.message)
            self.pause()
            return

        railway_trains = result.data
        for i, (railway, train) in enumerate(railway_trains):
            print(
                f"[{i + 1}] {train.name} | {railway.route} | {len(railway.stations)} stations | Cap: {train.capacity} | Price: {train.ticket_price} | Quality: {train.quality_index}/10"
            )

        print(f"\nYour wallet balance: {self._customer.wallet.balance}")

        choice = self.get_required_feedback("\nSelect a train: ")
        if choice is None:
            self.cancel_operation(controller)
            return

        try:
            _, train = railway_trains[int(choice) - 1]
        except (ValueError, IndexError):
            self.invalid_input()
            self.pause()
            return

        destination = self.get_required_feedback("Destination station: ")
        if destination is None:
            self.cancel_operation(controller)
            return

        quantity = self.get_required_feedback("Number of tickets: ")
        if quantity is None:
            self.cancel_operation(controller)
            return

        try:
            quantity = int(quantity)
        except ValueError:
            self.invalid_input()
            self.pause()
            return

        result = controller.services.ticket.buy_ticket(
            self._customer.id, train.name, destination, quantity
        )
        print(result.message)
        if result.success:
            export_result = controller.services.ticket.export_tickets_to_file(
                "tickets.txt"
            )
            print(export_result.message)
            print(f"\nYour current wallet balance: {self._customer.wallet.balance}")

        self.pause()

    def list_tickets(self, controller: MenuController) -> None:
        result = controller.services.ticket.get_customer_tickets(self._customer)
        if not result.success:
            print("No tickets have been bought.")
            self.pause()
            return

        for ticket, train in result.data:
            ticket_info = ticket.get_str(self._customer, train)
            print(ticket_info)
        self.pause()
