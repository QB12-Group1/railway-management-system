from enum import StrEnum

from app.models.base import Model
from app.models.wallet import Wallet


class UserRole(StrEnum):
    """
    Enumeration of user roles within the system.

    The role determines the level of access and permissions assigned
    to a user.

    Attributes:
        ADMIN: Administrator with elevated privileges.
        STAFF: Staff member with operational permissions.
        CUSTOMER: Customer account used for client access.
    """

    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"


class User(Model):
    """
    Base user model.

    Represents a generic user account containing shared attributes
    such as a unique identifier, username, password, and role.

    Args:
        username (str): The user's login username.
        password (str): The user's password.
        role (UserRole): The role assigned to the user.
    """

    def __init__(self, username: str, password: str, role: UserRole) -> None:
        super().__init__()
        self.username = username
        self.password = password
        self.role = role


class Admin(User):
    """
    Administrator user.

    Represents a user with administrative privileges.
    """

    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password, UserRole.ADMIN)


class Staff(User):
    """
    Staff user.

    Represents an internal staff member with operational permissions.
    """

    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password, UserRole.STAFF)


class Customer(User):
    """
    Customer user.

    Extends the base user model with additional personal information
    and an associated wallet used to manage the customer's balance.

    Args:
        username (str): The user's login username.
        password (str): The user's password.
        full_name (str): The customer's full name.
        email (str): The customer's email address.

    Attributes:
        full_name (str): The customer's full name.
        email (str): The customer's email address.
        wallet (Wallet): Wallet instance associated with the customer for managing funds and transactions.
    """

    def __init__(
        self, username: str, password: str, full_name: str, email: str
    ) -> None:
        super().__init__(username, password, UserRole.CUSTOMER)
        self.full_name = full_name
        self.email = email
        self.wallet = Wallet()
