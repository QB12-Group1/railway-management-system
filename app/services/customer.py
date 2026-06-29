from app.models.user import Customer
from app.repositories.user import UserRepository
from app.services.base import Service, ServiceResult
from app.utils.validators import (
    INVALID_PASSWORD_MESSAGE,
    invalid_email_message,
    validate_email,
    validate_password,
)


class CustomerService(Service):
    """
    Service responsible for handling customer profile management.

    This service manages customer account updates and acts as the
    intermediary between the Customer controllers and the UserRepository.

    Dependencies:
        UserRepository: For retrieving and updating customer data.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """
        Initialize the CustomerService.

        Args:
            user_repository (UserRepository): The repository instance used for user persistence.
        """
        self.user_repository = user_repository

    def update_profile(
        self,
        username: str,
        new_full_name: str | None = None,
        new_email: str | None = None,
        new_password: str | None = None,
    ) -> ServiceResult[Customer]:
        """
        Update a customer's profile information.

        Only fields that are provided will be updated.
        Ensures email uniqueness before applying changes.

        Args:
            username (str): The username of the customer to update.
            new_full_name (str | None): New full name, if provided.
            new_email (str | None): New email address, if provided.
            new_password (str | None): New password, if provided.

        Returns:
            ServiceResult[Customer]: A success result with the updated Customer,
            or a failure result if validation fails.
        """
        user = self.user_repository.get_by_username(username)

        if user is None:
            return self.failure(f"User '{username}' not found.")

        if not isinstance(user, Customer):
            return self.failure(f"User '{username}' is not a customer member.")

        if new_email is not None and new_email != user.email:
            if not validate_email(new_email):
                message = invalid_email_message(new_email)
                return self.failure(message)
            if self.user_repository.exists_by_email(new_email):
                return self.failure(f"Email '{new_email}' is already taken.")

        if (
            new_password is not None
            and new_password != user.password
            and not validate_password(new_password)
        ):
            return self.failure(INVALID_PASSWORD_MESSAGE)

        self.user_repository.update_by_username(
            username, password=new_password, full_name=new_full_name, email=new_email
        )
        return self.success("Profile updated successfully.", user)
