from typing import TYPE_CHECKING

from app.menus.base import BaseMenu
from app.menus.railway_menu import RailwayManagementMenu
from app.menus.train_menu import TrainManagementMenu

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class StaffDashboard(BaseMenu):
    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Staff Operations Dashboard",
            {
                "Manage Railways": lambda controller: controller.push(
                    RailwayManagementMenu()
                ),
                "Manage Trains": lambda controller: controller.push(
                    TrainManagementMenu()
                ),
                "Exit": lambda controller: controller.pop(),
            },
        )
