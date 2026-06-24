from app.models.user import Customer, User
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    """
    Repository for managing all user types in the system.

    This repository extends the base Repository with user-specific
    operations. Users are primarily identified by their unique username.
    """

    def get_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their unique username.

        Args:
            username (str): The username to search for.

        Returns:
            User | None: The matching user if found, otherwise None.
        """
        for user in self.items:
            if user.username == username:
                return user
        return None

    def get_by_email(self, email: str) -> Customer | None:
        """
        Retrieve a customer by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            Customer | None: The matching customer if found, otherwise None.
        """
        for user in self.items:
            if isinstance(user, Customer) and user.email == email:
                return user
        return None

    def exists_by_username(self, username: str) -> bool:
        """
        Check whether a user with the given username exists.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if a user with the username exists, otherwise False.
        """
        return self.get_by_username(username) is not None

    def exists_by_email(self, email: str) -> bool:
        """
        Check whether a customer with the given email exists.

        Args:
            email (str): The email address to check.

        Returns:
            bool: True if a customer with the email exists, otherwise False.
        """
        return self.get_by_email(email) is not None

    def remove_by_username(self, username: str) -> bool:
        """
        Remove a user from the repository using their username.

        Args:
            username (str): The username of the user to remove.

        Returns:
            bool: True if the user was removed, otherwise False.
        """
        user = self.get_by_username(username)

        if user is None:
            return False

        return self.remove(user)

    def update_by_username(
        self,
        username: str,
        password: str | None = None,
        full_name: str | None = None,
        email: str | None = None,
    ) -> bool:
        """
        Update an existing user using their username.

        Only the fields provided will be modified. For Customer-specific
        fields such as full_name and email, the update is only applied if
        the user instance is a Customer.

        Args:
            username (str): The username of the user to update.
            password (str | None): New password, if provided. Defaults to None.
            full_name (str | None): New full name, if provided (Customer only). Defaults to None.
            email (str | None): New email address, if provided (Customer only). Defaults to None.

        Returns:
            bool: True if the user was updated, otherwise False.
        """
        user = self.get_by_username(username)

        if user is None:
            return False

        if password is not None:
            user.password = password

        if isinstance(user, Customer):
            if full_name is not None:
                user.full_name = full_name
            if email is not None:
                user.email = email

        return True
