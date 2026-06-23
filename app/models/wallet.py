class Wallet:
    """
    Represents a user's wallet containing a balance and an optional linked card.

    Attributes:
        balance (float): The current balance stored in the wallet.
        linked_card (str | None): Identifier of the linked card associated with the wallet. This will be replaced with a DebitCard object once that model is implemented.
    """

    def __init__(self, balance: float = 0.0, linked_card: str | None = None) -> None:
        """
        Initialize a Wallet instance.

        Args:
            balance (float, optional): Initial wallet balance. Defaults to 0.0.
            linked_card (str | None, optional): Identifier for a linked card. Defaults to None.
        """
        self.balance = balance
        self.linked_card = linked_card  # TODO: Replace str with DebitCard once the DebitCard model is implemented
