class Wallet:
    def __init__(self, balance: float = 0.0, linked_card: str | None = None) -> None:
        self.balance = balance
        self.linkedCard = linked_card
