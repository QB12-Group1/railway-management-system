from typing import TYPE_CHECKING

from app.menus.base import BaseMenu

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class RailwayManagementMenu(BaseMenu):
    """Menu for managing railway by staff members."""

    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Manage Railways",
            {
                "Add railway": self.add_railway,
                "Remove railway": self.remove_railway,
                "Modify railway": self.modify_railway,
                "List railway": self.list_railway,
                "Exit": lambda controller: controller.pop(),
            },
        )

    def add_railway(self, controller: MenuController) -> None:
        self.show_title("Register")

        name = self.get_required_feedback("Railway name: ")

        if name is None:
            self.cancel_operation(controller)
            return

        origin = self.get_required_feedback("Origin station: ")
        if origin is None:
            self.cancel_operation(controller)
            return

        destination = self.get_required_feedback("Distination station: ")
        if destination is None:
            self.cancel_operation(controller)
            return

        stations_input = self.get_required_feedback("Stations: ")
        if stations_input is None:
            self.cancel_operation(controller)
            return

        travel_distance = self.get_required_feedback("Travel distance (km): ")
        if travel_distance is None:
            self.cancel_operation(controller)
            return
        try:
            travel_distance = int(travel_distance)
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            self.pause()
            return

        stations = [s.strip() for s in stations_input.split(",")]

        result = controller.services.staff.add_railway(
            name, origin, destination, stations, travel_distance
        )

        print(result.message)
        self.pause()

    # TODO: ask if the user is sure about this operation also print a message saying with this change these trains aren't operatable unless you modify them to operate on other lanes
    def remove_railway(self, controller: MenuController) -> None:
        self.show_title("Remove")

        name = self.get_required_feedback("Railway name: ")

        if name is None:
            self.cancel_operation(controller)
            return

        result = controller.services.staff.remove_railway(name)
        print(result.message)
        self.pause()

    def modify_railway(self, controller: MenuController) -> None:
        self.show_title("Update")

        name = self.get_required_feedback("Railway name: ")

        if name is None:
            self.cancel_operation(controller)
            return

        print("Leave blank to Keep current value.")
        new_name = self.get_feedback("New name: ") or None
        if new_name is not None and self.is_cancel_command(new_name):
            self.cancel_operation(controller)
            return

        new_origin = self.get_feedback("New origin: ") or None
        if new_origin is not None and self.is_cancel_command(new_origin):
            self.cancel_operation(controller)
            return

        new_destination = self.get_feedback("New destination: ") or None
        if new_destination is not None and self.is_cancel_command(new_destination):
            self.cancel_operation(controller)
            return

        new_stations = self.get_feedback("New stations: ")
        stations = (
            [s.strip() for s in new_stations.split(",")] if new_stations else None
        )
        if stations and self.is_cancel_command(stations[0]):
            self.cancel_operation(controller)
            return

        result = controller.services.staff.update_railway(
            name, new_name, new_origin, new_destination, stations
        )
        print(result.message)
        self.pause()

    def list_railway(self, controller: MenuController) -> None:
        self.show_title("Railway List")

        result = controller.services.staff.get_all_railways()

        # TODO: pretty print this section
        if not result.data:
            print("No railway found.")
            self.pause()
            return

        for railway in result.data:
            print(railway)

        self.pause()
