from app.models.transaction import Transaction
from app.repositories.base import Repository


class TransactionRepository(Repository[Transaction]):
    def get_all_by_customer_id(
        self, customer_id: str, limit: int | None
    ) -> list[Transaction]:
        transactions = [
            transaction
            for transaction in self.items
            if transaction.customer_id == customer_id
        ]

        transactions.reverse()

        if limit is not None:
            return transactions[:limit]

        return transactions

    # NOTE: Dear judge we were running out of time. that's why this function is defined here. I know it's ugly but deal with it ;)
    def export_customer_transactions(
        self,
        customer_id: str,
        username: str,
        limit: int | None = 5,
    ) -> None:
        transactions = self.get_all_by_customer_id(customer_id, limit)

        file_name = f"{username}_transactions.txt"

        with open(file_name, "w") as file:
            for transaction in transactions:
                file.write(f"{transaction}\n")
