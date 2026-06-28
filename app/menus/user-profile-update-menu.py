from typing import TYPE_CHECKING

from app.menus.base import BaseMenu

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class UserProfileUpdate(BaseMenu):
    def __init__(self, customer):
        self.customer = customer

    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Manage Staff",
            {
                "Show Profile User": self.show_profile_user,
                "Update User Profile": self.update_user,
                "Exit": lambda controller: controller.pop(),
            },
        )

    def show_profile_user(self, controller: MenuController):
        self.show_title(" Show Profile Customer")
        self.show_options(self.customer)
        controller.services.customer.success("Showing Success in Profile")
        self.pause()

    def update_user(self, controller: MenuController):
        username = self.get_required_feedback("New Username : ")
        if username is None:
            self.cancel_operation(controller)
            return

        password = self.get_required_feedback("New Password: ")
        if password is None:
            self.cancel_operation(controller)
            return

        full_name = self.get_required_feedback("New Full Name: ")
        if full_name is None:
            self.cancel_operation(controller)
            return

        email = self.get_required_feedback("New Email: ")
        if email is None:
            self.cancel_operation(controller)
            return

        controller.services.customer.update_profile(username, full_name, email)
        controller.services.customer.update_password(username, password)
        self.pause()
