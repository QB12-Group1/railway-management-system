from app.models.transaction import Transaction
from app.repositories.base import Repository


class TransactionRepository(Repository[Transaction]):
    def get_by_customer_id(
        self, customer_id: str, limit: int | None
    ) -> list[Transaction]:
        transactions = [t for t in self.items if t.customer_id == customer_id]

        transactions.reverse()

        if limit is not None:
            return transactions[:limit]

        return transactions
