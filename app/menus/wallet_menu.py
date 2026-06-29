from typing import TYPE_CHECKING

from app.menus.base import BaseMenu
from app.models.user import Customer

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class WalletMenu(BaseMenu):
    def __init__(self, customer: Customer) -> None:
        self._customer = customer

    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            f"Wallet[{self._customer.wallet.balance}]",
            {
                "Charge Wallet": self.charge_wallet,
                "Link Card": self.link_card,
                "My Card": self.show_card,
                "Show Transactions": self.show_transactions,
                "Go back": lambda controller: controller.pop(),
            },
        )

    def charge_wallet(self, controller: MenuController) -> None:
        self.show_title("Charge Wallet")

        print(f"Current balance: {self._customer.wallet.balance}")

        if self._customer.wallet.linked_card is None:
            print("No card linked. Please link a card first.")
            self.pause()
            self.link_card(controller)
            return

        amount = self.get_required_feedback("Amount to charge: ")
        if amount is None:
            self.cancel_operation(controller)
            return

        try:
            amount = float(amount)
        except ValueError:
            print("Invalid amount! Please enter a positive number.")
            self.pause()
            return

        result = controller.services.wallet.charge_wallet(
            self._customer.username, amount
        )
        print(result.message)
        self.pause()

    def link_card(self, controller: MenuController) -> None:
        if self._customer.wallet.linked_card is not None:
            print("A card is already linked to this wallet.")
            self.pause()
            return

        self.show_title("Link Card")

        card_number = self.get_required_feedback("Card number (16 digits): ")
        if card_number is None:
            self.cancel_operation(controller)
            return

        exp_month = self.get_required_feedback("Expiration month (1-12): ")
        if exp_month is None:
            self.cancel_operation(controller)
            return

        exp_year = self.get_required_feedback("Expiration year (1403-1408): ")
        if exp_year is None:
            self.cancel_operation(controller)
            return

        pin = self.get_required_feedback("PIN (6 digits): ")
        if pin is None:
            self.cancel_operation(controller)
            return

        cvv2 = self.get_required_feedback("CVV2 (3 digits): ")
        if cvv2 is None:
            self.cancel_operation(controller)
            return

        try:
            exp_month = int(exp_month)
            exp_year = int(exp_year)
            if 3 <= exp_year <= 8:
                exp_year += 1400
        except ValueError:
            print("Invalid expiration date.")
            self.pause()
            return

        result = controller.services.wallet.link_card(
            self._customer.username,
            card_number,
            exp_month,
            exp_year,
            pin,
            cvv2,
        )
        print(result.message)
        self.pause()

    def show_card(self, _: MenuController) -> None:
        self.show_title("My Card")

        card = self._customer.wallet.linked_card
        if card is None:
            print("No card linked to this wallet.")
            self.pause()
            return

        masked = "**** **** **** " + card.card_number[-4:]
        print(f"Card number: {masked}")
        print(
            f"Expiry: {card.expiration_year}/{('0' if card.expiration_month < 10 else '') + str(card.expiration_month)}"
        )
        self.pause()

    def show_transactions(self, controller: MenuController) -> None:
        self.show_title("Recent Transactions (Last 5)")

        result = controller.services.wallet.get_transactions(self._customer.id)

        if not result.success or not result.data:
            print(result.message)
            self.pause()
            return

        for transaction in result.data:
            print(transaction)

        self.pause()
