from app.models.debit_card import DebitCard
from app.repositories.user_repository import UserRepository
from app.services.base import BaseService, ServiceResult


class WalletService(BaseService):
    

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def link_card(self, username: str, card_details: dict) -> ServiceResult:
        
        user = self._user_repository.get_by_username(username)
        if user is None:
            return self.failure(f"User '{username}' not found.")

        try:
            card = DebitCard(
                card_number=card_details["card_number"],
                expiration_month=card_details["expiration_month"],
                expiration_year=card_details["expiration_year"],
                pin=card_details["pin"],
                cvv2=card_details["cvv2"],
            )
        except (ValueError, KeyError) as e:
            return self.failure(f"Invalid card details: {e}")

        user.wallet.linked_card = card
        return self.success("Card linked successfully.", data=card)

    def charge_wallet(self, username: str, amount: float) -> ServiceResult:
        
        user = self._user_repository.get_by_username(username)
        if user is None:
            return self.failure(f"User '{username}' not found.")

        if user.wallet.linked_card is None:
            return self.failure("No debit card linked to this wallet.")

        if amount <= 0:
            return self.failure("Charge amount must be positive.")

        user.wallet.balance += amount
        return self.success(
            f"Wallet charged successfully. New balance: {user.wallet.balance}",
            data=user.wallet.balance,
        )