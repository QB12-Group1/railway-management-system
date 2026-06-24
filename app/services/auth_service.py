from typing import TypeVar

from app.models.user import Admin, Customer, Staff, User
from app.repositories.user import UserRepository
from app.services.base import Service, ServiceResult

TUser = TypeVar("TUser", bound=User)


class AuthenticationService(Service):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register_user(
        self, user: TUser, email: str | None = None
    ) -> ServiceResult[TUser]:
        if self.user_repository.exists_by_username(user.username):
            return self.failure(f"Username {user.username} is already taken.")

        if email and self.user_repository.exists_by_email(email):
            return self.failure(f"Email {email} is already taken.")

        self.user_repository.add(user)
        return self.success("Registration successful!", user)

    def register_admin(self, username: str, password: str) -> ServiceResult[Admin]:
        new_admin = Admin(username, password)
        return self.register_user(new_admin)

    def register_staff(self, username: str, password: str) -> ServiceResult[Staff]:
        new_staff = Staff(username, password)
        return self.register_user(new_staff)

    def register_customer(
        self, username: str, password: str, full_name: str, email: str
    ) -> ServiceResult[Customer]:
        new_customer = Customer(username, password, full_name, email)
        return self.register_user(new_customer, email)

    def log_in(self, username: str, password: str) -> ServiceResult[User]:
        user = self.user_repository.get_by_username(username)

        if not user:
            return self.failure("User not found.")

        if user.password != password:
            return self.failure("Password doesn't match.")

        return self.success("Login successful.", user)
