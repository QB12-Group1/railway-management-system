from typing import TypeVar

from app.models.user import Admin, Customer, Staff, User
from app.repositories.user import UserRepository
from app.services.base import Service, ServiceResult

TUser = TypeVar("TUser", bound=User)


class AuthenticationService(Service):
    """
    Service responsible for handling user authentication and registration.

    This service coordinates with the `UserRepository` to manage user creation
    (registration) and identity verification (login) for various user roles.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """
        Initialize the AuthenticationService.

        Args:
            user_repository (UserRepository): The repository instance used for user persistence.
        """
        self.user_repository = user_repository

    def register_user(
        self, user: TUser, email: str | None = None
    ) -> ServiceResult[TUser]:
        """
        Register a new user in the system.

        Checks for existing usernames and emails before adding the user to the
        repository.

        Args:
            user (TUser): The user instance to register.
            email (str | None): Optional email to validate for uniqueness. Defaults to None.

        Returns:
            ServiceResult[TUser]: A success result containing the user if registration
            succeeds, or a failure result if validation fails.
        """
        if self.user_repository.exists_by_username(user.username):
            return self.failure(f"Username {user.username} is already taken.")

        if email and self.user_repository.exists_by_email(email):
            return self.failure(f"Email {email} is already taken.")

        self.user_repository.add(user)
        return self.success("Registration successful!", user)

    def register_admin(self, username: str, password: str) -> ServiceResult[Admin]:
        """
        Register a new admin user.

        Args:
            username (str): The admin's unique username.
            password (str): The admin's password.

        Returns:
            ServiceResult[Admin]: A success result with the Admin instance,
            or a failure result.
        """
        new_admin = Admin(username, password)
        return self.register_user(new_admin)

    def register_staff(
        self, username: str, password: str, full_name: str, email: str
    ) -> ServiceResult[Staff]:
        """
        Register a new staff user.

        Args:
            username (str): The staff's unique username.
            password (str): The staff's password.
            full_name (str): The staff's full name.
            email (str): The staff's email address.

        Returns:
            ServiceResult[Staff]: A success result with the Staff instance,
            or a failure result.
        """
        new_staff = Staff(username, password, full_name, email)
        return self.register_user(new_staff, email)

    def register_customer(
        self, username: str, password: str, full_name: str, email: str
    ) -> ServiceResult[Customer]:
        """
        Register a new customer user.

        Args:
            username (str): The customer's unique username.
            password (str): The customer's password.
            full_name (str): The customer's full name.
            email (str): The customer's email address.

        Returns:
            ServiceResult[Customer]: A success result with the Customer instance,
            or a failure result.
        """
        new_customer = Customer(username, password, full_name, email)
        return self.register_user(new_customer, email)

    def log_in(self, username: str, password: str) -> ServiceResult[User]:
        """
        Authenticate a user by username and password.

        Args:
            username (str): The username to authenticate.
            password (str): The password to verify.

        Returns:
            ServiceResult[User]: A success result containing the User if credentials
            are correct, or a failure result if the user is not found or the
            password is incorrect.
        """
        user = self.user_repository.get_by_username(username)

        if not user:
            return self.failure("User not found.")

        if user.password != password:
            return self.failure("Password doesn't match.")

        return self.success("Login successful.", user)
