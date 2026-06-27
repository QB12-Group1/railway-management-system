from app.models.user import Staff
from app.repositories.user import UserRepository
from app.services.auth import AuthenticationService
from app.services.base import Service, ServiceResult


class AdminService(Service):
    """
    Service responsible for handling all administrator operations.

    This service manages staff accounts and acts as the intermediary
    between the Admin controllers and the UserRepository.
    It delegates user creation and validation to the AuthenticationService.

    Dependencies:
        UserRepository: For retrieving and removing users.
        AuthenticationService: For registering new staff members.
    """

    def __init__(
        self, user_repository: UserRepository, auth_service: AuthenticationService
    ) -> None:
        """
        Initialize the AdminService.

        Args:
            user_repository (UserRepository): The repository instance used for user persistence.
            auth_service (AuthenticationService): The service used for registering new users.
        """
        self.user_repository = user_repository
        self.auth_service = auth_service

    def add_staff(
        self, username: str, password: str, full_name: str, email: str
    ) -> ServiceResult[Staff]:
        """
        Add a new staff member to the system.

        Delegates registration and validation to the AuthenticationService.

        Args:
            username (str): The staff's unique username.
            password (str): The staff's password.
            full_name (str): The staff's full name.
            email (str): The staff's email address.

        Returns:
            ServiceResult[Staff]: A success result containing the created
            Staff instance, or a failure result if validation fails or
            the staff object cannot be created.
        """
        new_staff = self.auth_service.register_staff(
            username, password, full_name, email
        )

        if not new_staff.success:
            return self.failure(new_staff.message)

        if new_staff.data is None:
            return self.failure("Failed to create staff.")

        return self.success(
            f"Train '{new_staff.data.username}' has been registered successfully.",
            new_staff.data,
        )

    def remove_staff(self, username: str) -> ServiceResult[None]:
        """
        Remove a staff member from the system.

        Args:
            username (str): The username of the staff member to remove.

        Returns:
            ServiceResult[None]: A success result if removed,
            or a failure result if not found or not a staff member.
        """
        user = self.user_repository.get_by_username(username)

        if user is None:
            return self.failure(f"User '{username}' not found.")

        if not isinstance(user, Staff):
            return self.failure(f"User '{username}' is not a staff member.")

        self.user_repository.remove(user)
        return self.success(f"Staff '{user.username}' has been removed successfully.")

    def get_all_staff(self) -> ServiceResult[list[Staff]]:
        """
        Retrieve all staff members in the system.

        Returns:
            ServiceResult[list[Staff]]: A success result containing
            a list of all staff members.
        """
        users = self.user_repository.get_all()
        staffs = [user for user in users if isinstance(user, Staff)]
        return self.success("All staffs have been retrieved.", staffs)
