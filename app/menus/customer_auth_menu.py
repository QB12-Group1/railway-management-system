from typing import TYPE_CHECKING

from app.menus.base import BaseMenu
from app.menus.customer_login_menu import CustomerLoginMenu

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class CustomerAuthMenu(BaseMenu):
    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Customer Authentication Menu",
            {
                "Register": self.show_not_implemented,  # TODO: implement user registeration menu
                "Log-in": lambda controller: controller.push(CustomerLoginMenu()),
                "Go back": lambda controller: controller.pop(),
            },
        )
