from typing import TYPE_CHECKING

from app.menus.base import BaseMenu
from app.models.user import Customer

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class TicketPurchaseMenu(BaseMenu):
    def __init__(self, customer: Customer) -> None:
        self.customer = customer

    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Ticket Purchase Menu",
            {
                "Viem trains & Buy ticket": self.Buy_ticket,
                "Exit": lambda controller: controller.pop(),
            },
        )

    def Buy_ticket(self, controller: MenuController) -> None:
        self.show_title("Available Trains")

        result = controller.services.ticket.get_available_trains()

        if not result.message or not result.data:
            print(result.message)
            self.pause()
            return

        trains = result.data

        for i, (railway, train) in enumerate(trains):
            print(f"[{i + 1}] Name: {train.name}")
            print(f"Origin: {railway.origin}")
            print(f"Destination: {railway.destination}")
            print(f"Stations: {', '.join(railway.stations)}")
            print(f"Capacity: {train.capacity} seats")
            print(f"Ticket price:  {train.ticket_price}")
            print(f"Quality index: {train.quality_index}/10")

        print(f"\nYour wallet balance: {self.customer.wallet.balance}")

        choice = self.get_required_feedback("\n Select a train: ")
        if choice is None:
            self.cancel_operation(controller)
            return

        try:
            _, train = trains[int(choice) - 1]
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
            self.customer.id, train.name, destination, quantity
        )

        print(result.message)

        if result.success:
            export_result = controller.services.ticket.export_tickets_to_file(
                "tickets.txt"
            )
            print(export_result.message)

        self.pause()
