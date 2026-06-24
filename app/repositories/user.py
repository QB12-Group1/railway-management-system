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
        Retrieve a user by their username.

        Args:
            username: The username to search for.

        Returns:
            The matching user if found, otherwise None.
        """
        for user in self.items:
            if user.username == username:
                return user
        return None

    def exists_by_username(self, username: str) -> bool:
        """
        Check whether a user with the given username exists.

        Args:
            username: The username to check.

        Returns:
            True if a user with the username exists, otherwise False.
        """
        return self.get_by_username(username) is not None

    def remove_by_username(self, username: str) -> bool:
        """
        Remove a user from the repository using their username.

        Args:
            username: The username of the user to remove.

        Returns:
            True if the user was removed, otherwise False.
        """
        user = self.get_by_username(username)

        if user is None:
            return False

        self.remove(user)
        return True

    def modify_by_usrename(
        self,
        username: str,
        password: str | None = None,
        full_name: str | None = None,
        email: str | None = None,
    ) -> bool:
        """
        Modify an existing user using their username.

        Only fields that are provided will be updated.
        For Customer-specific fields such as full_name and email,
        the update is only applied if the user is a Customer.

        Args:
            username: The username of the user to modify.
            password: New password, if provided.
            full_name: New full name, if provided (Customer only).
            email: New email address, if provided (Customer only).

        Returns:
            True if the user was modified, otherwise False.
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
