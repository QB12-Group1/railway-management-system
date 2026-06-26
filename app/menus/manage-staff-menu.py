from app.menu_controller import MenuController
from app.menus.base import BaseMenu
from app.menus.main_menu import MainMenu
from app.repositories.user import User
from app.services.admin import AdminService


class ManageStaff(BaseMenu):
    def show_admin_manage(
        self,
        user: User,
        admin: AdminService,
        menu: MainMenu,
        controler: MenuController,
        username,
        password,
        full_name,
        email,
    ):
        username = user.username
        password = user.password

        if user.role == "admin":
            while True:
                print("===== Manage Staff =====")
                print("1. Add Staff")
                print("2. Remove Staff")
                print("3. View Staff Members")
                print("4. Exit")

                choice = input("Select an option: ")

                if choice == "1":
                    admin.add_staff(username, password, full_name, email)
                elif choice == "2":
                    admin.remove_staff(username)

                elif choice == "3":
                    admin.get_all_staff()

                elif choice == "4":
                    print("Returning to Main Menu...")
                    break

                else:
                    print("Invalid option.")

        menu.display(controler)
