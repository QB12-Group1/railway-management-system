import time

from app.models.debit_card import DebitCard
from app.models.transaction import Transaction, TransactionType
from app.models.user import Customer
from app.repositories.transaction import TransactionRepository
from app.repositories.user import UserRepository
from app.services.base import Service, ServiceResult


class WalletService(Service):
    """
    Service responsible for managing customer wallets and payment methods.

    This service handles the linking of debit cards to customer accounts
    , manages balance-related operations and records all transactons .
    """

    def __init__(
        self,
        user_repository: UserRepository,
        transaction_repository: TransactionRepository,
    ) -> None:
        """
        Initialize the WalletService.

        Args:
            user_repository (UserRepository): The repository used to retrieve and update users.
            transaction_Repository (TransactionRepository):Repository for transactions.
        """
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository

    def link_card(
        self,
        username: str,
        card_number: str,
        expiration_month: int,
        expiration_year: int,
        pin: str,
        cvv2: str,
    ) -> ServiceResult[DebitCard]:
        """
        Link a debit card to a customer's wallet.

        Validates the user's existence and role, then attempts to create a
        DebitCard instance. If valid, the card is attached to the customer's wallet.

        Args:
            username (str): The username of the customer.
            card_number (str): The 16-digit card number.
            expiration_month (int): The card's expiration month.
            expiration_year (int): The card's expiration year.
            pin (str): The card's 6-digit PIN.
            cvv2 (str): The card's 3-digit security code.

        Returns:
            ServiceResult[DebitCard]: A success result with the linked DebitCard
            instance, or a failure result if validation or creation fails.
        """
        user = self.user_repository.get_by_username(username)

        if user is None:
            return self.failure(f"User '{username}' not found.")

        if not isinstance(user, Customer):
            return self.failure(f"User '{username}' is not a customer member.")

        try:
            card = DebitCard(card_number, expiration_month, expiration_year, pin, cvv2)
        except ValueError as e:
            return self.failure(f"Invalid card information: {e}")

        user.wallet.link(card)
        return self.success("Card linked to wallet successfully.", card)

    def charge_wallet(self, username: str, amount: float) -> ServiceResult[float]:
        """
        Increase the balance of a customer's wallet and record the transaction.

        Args:
            username (str): The username of the customer.
            amount (float): The amount of money to add to the wallet.

        Returns:
            ServiceResult[float]: A success result containing the new wallet balance,
            or a failure result if the user is invalid, no card is linked, or
            the amount is non-positive.
        """
        user = self.user_repository.get_by_username(username)

        if user is None:
            return self.failure(f"User '{username}' not found.")

        if not isinstance(user, Customer):
            return self.failure(f"User '{username}' is not a customer member.")

        if user.wallet.linked_card is None:
            return self.failure("No debit card linked to this wallet.")

        if amount <= 0:
            return self.failure("Charge amount must be positive.")

        user.wallet.charge(amount)

        return self.success(
            f"Wallet charged successfully. New balance: {user.wallet.balance}",
            user.wallet.balance,
        )

    def get_transaction(self, customer_id: str) -> ServiceResult[list[Transaction]]:
        transactions = self.transaction_repository.get_by_customer_id(
            customer_id, limit=5
        )

        if not transactions:
            return self.failure("No transaction found")

        return self.success(
            f"Found{len(transactions)} recent transaction(s).", transactions
        )

    def save_transaction(
        self,
        customer_id: str,
        amount: float,
        transaction_type: TransactionType,
        balance_after: float,
    ) -> None:
        t = time.strftime("%Y-%m-%d | %H:%M:%S", time.localtime())

        transaction = Transaction(
            customer_id,
            amount,
            transaction_type,
            balance_after,
            t,
        )

        self.transaction_repository.add(transaction)
