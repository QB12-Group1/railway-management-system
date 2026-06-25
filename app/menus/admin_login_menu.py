from app.menu_controller import MenuController
from app.menus.base import BaseMenu


class AdminLoginMenu(BaseMenu):
    def display(self, controller: MenuController) -> None:
        admin_username, admin_password = "admin", "admin"
        result = controller.services.auth.register_admin(admin_username, admin_password)
        if not result.success:
            print(result.message)
            self.invalid_input()
            return
