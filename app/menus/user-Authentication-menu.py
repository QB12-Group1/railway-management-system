from __future__ import annotations
from typing import TYPE_CHECKING
from app.menus.base import BaseMenu
from app.menus.customer_login_menu import CustomerLoginMenu

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class UserAuthenticationMenu(BaseMenu):
    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "User Authentication Menu",
            {
                "Register": self.show_not_implemented,
                "Log in": lambda controller: controller.push(CustomerLoginMenu()),
                "Exit": lambda controller: controller.pop(),
            },
        )