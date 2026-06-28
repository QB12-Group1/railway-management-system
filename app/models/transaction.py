from enum import StrEnum

from app.models.base import Model


class TransactionType(StrEnum):
    CHARGE = "charge"
    PURCHASE = "purchase"


class Transaction(Model):
    def __init__(
        self,
        customer_id: str,
        amount: float,
        transaction_type: TransactionType,
        balance_after: float,
        t: str,
    ) -> None:
        super().__init__()
        self.customer_id = customer_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.balance_after = balance_after
        self.time = t

    def __str__(self) -> str:
        sign = "+" if self.amount > 0 else ""
        return (
            f"{self.time} | "
            f"Type: {self.transaction_type.value:10} | "
            f"Amount: {sign}{self.amount:.2f}"
            f"Balance: {self.balance_after:.2f}"
        )
