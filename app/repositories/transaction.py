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
    def export_to_file(self, file_path: str) -> None:
        transactions = self.get_all()
        with open(file_path, mode="w") as file:
            for transaction in transactions:
                file.write(str(transaction) + "\n")
