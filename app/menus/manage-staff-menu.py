from typing import TYPE_CHECKING

from app.menus.base import BaseMenu

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class ManageStaff(BaseMenu):
    """Manage Staff Menu"""

    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Manage Staff",
            {
                "Add Staff": self.add_staff,
                "Remove Staff": self.remove_staff,
                "List Staff": self.list_staff,
                "Exit": lambda controller: controller.pop(),
            },
        )

    def add_staff(self, controller: MenuController) -> None:
        self.show_title("Add Staff")

        username = self.get_required_feedback("Staff username: ")

        if username is None:
            self.cancel_operation(controller)
            return

        password = self.get_required_feedback("Staff Password: ")
        if password is None:
            self.cancel_operation(controller)
            return

        full_name = self.get_required_feedback("Full Name Staff: ")
        if full_name is None:
            self.cancel_operation(controller)
            return

        email = self.get_required_feedback("Email: ")
        if email is None:
            self.cancel_operation(controller)
            return

        action = controller.services.admin.add_staff(
            username, password, full_name, email
        )
        print(action.message)
        self.pause()

    def remove_staff(self, controller: MenuController) -> None:
        self.show_title("Remove Staff")

        username = self.get_required_feedback(" Username: ")

        if username is None:
            self.cancel_operation(controller)
            return

        action = controller.services.admin.remove_staff(username)
        print(action.message)
        self.pause()

    def list_staff(self, controller: MenuController) -> None:
        self.show_title("Staff List")

        action = controller.services.admin.get_all_staff()

        if not action.data:
            print("No Staff found.")
            self.pause()
            return

        for staff in action.data:
            print(staff)

        self.pause()
