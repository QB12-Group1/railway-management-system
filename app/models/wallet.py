from app.models.base import Model
from app.models.debit_card import DebitCard


class Wallet(Model):
    """
    Represents a user's wallet containing a balance and an optional linked card.

    Attributes:
        balance (float): The current balance stored in the wallet.
        linked_card (DebitCard | None): Identifier of the linked card associated with the wallet. This will be replaced with a DebitCard object once that model is implemented.
    """

    def __init__(
        self, balance: float = 0.0, linked_card: DebitCard | None = None
    ) -> None:
        """
        Initialize a Wallet instance.

        Args:
            balance (float, optional): Initial wallet balance. Defaults to 0.0.
            linked_card (DebitCard | None, optional): Identifier for a linked card. Defaults to None.
        """
        super().__init__()
        self.balance = balance
        self.linked_card = linked_card

    def charge(self, amount: float) -> None:
        """
        Increase the wallet balance by a specified amount.

        Args:
            amount (float): The amount of money to add to the balance.
        """
        self.balance += amount

    def link(self, card: DebitCard) -> None:
        """
        Associate a debit card with the wallet.

        Args:
            card (DebitCard): The debit card instance to link.
        """
        self.linked_card = card
