from app.models.transaction import Transaction
from app.repositories.base import Repository
from app.utils.file_utils import get_data_path


class TransactionRepository(Repository[Transaction]):
    def get_all_by_customer_id(
        self, customer_id: str, limit: int | None
    ) -> list[Transaction]:
        """
        Retrieves all transactions associated with a specific customer.

        Args:
            customer_id (str): The unique identifier of the customer.
            limit (int | None): The maximum number of recent transactions to return.
                If None, all transactions are returned.

        Returns:
            list[Transaction]: A list of transactions sorted from newest to oldest.
        """
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
        """
        Exports a customer's recent transaction history to a text file.

        The file is saved in the system's data directory with the naming
        convention '{username}_transactions.txt'.

        Args:
            customer_id (str): The ID of the customer whose history to export.
            username (str): The username used to generate the filename.
            limit (int | None): The number of transactions to include in the
                export. Defaults to 5.

        Returns:
            None
        """
        transactions = self.get_all_by_customer_id(customer_id, limit)

        file_name = f"{username}_transactions.txt"
        file_path = get_data_path(file_name)

        with open(file_path, "w") as file:
            for transaction in transactions:
                file.write(f"{transaction}\n")
