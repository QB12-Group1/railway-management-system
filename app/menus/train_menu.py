from typing import TYPE_CHECKING

from app.menus.base import BaseMenu

if TYPE_CHECKING:
    from app.menu_controller import MenuController


class TrainManagementMenu(BaseMenu):
    """Menu for managing trains by staff members."""

    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Manage Train",
            {
                "Add train": self.add_train,
                "Remove train": self.remove_train,
                "Modify train": self.modify_train,
                "List train": self.list_trains,
                "Exit": lambda controller: controller.pop(),
            },
        )

    def add_train(self, controller: MenuController) -> None:
        self.show_title("Register")

        name = self.get_required_feedback("Train name: ")

        if name is None:
            self.cancel_operation(controller)
            return

        railway_id = self.get_required_feedback("Railway id: ")
        if railway_id is None:
            self.cancel_operation(controller)
            return

        average_velocity = self.get_required_feedback("Average velocity: ")
        if average_velocity is None:
            self.cancel_operation(controller)
            return

        stop_time = self.get_required_feedback("Stop time: ")
        if stop_time is None:
            self.cancel_operation(controller)
            return

        quality_index = self.get_required_feedback("Quality index: ")
        if quality_index is None:
            self.cancel_operation(controller)
            return

        ticket_price = self.get_required_feedback("Ticket price: ")
        if ticket_price is None:
            self.cancel_operation(controller)
            return

        capacity = self.get_required_feedback("Capacity: ")
        if capacity is None:
            self.cancel_operation(controller)
            return

        try:
            average_velocity = float(average_velocity)
            stop_time = float(stop_time)
            quality_index = float(quality_index)
            ticket_price = float(ticket_price)
            capacity = int(capacity)
        except ValueError:
            print("Invalid input! Please enter valid number.")
            self.pause()
            return

        result = controller.services.staff.add_train(
            name,
            railway_id,
            average_velocity,
            stop_time,
            quality_index,
            ticket_price,
            capacity,
        )
        print(result.message)
        self.pause()

    def remove_train(self, controller: MenuController) -> None:
        self.show_title("Remove")

        name = self.get_required_feedback("Railway name: ")

        if name is None:
            self.cancel_operation(controller)
            return

        result = controller.services.staff.remove_train(name)
        print(result.message)
        self.pause()

    def modify_train(self, controller: MenuController) -> None:
        self.show_title("Update")

        name = self.get_required_feedback("Train name: ")

        if name is None:
            self.cancel_operation(controller)
            return

        print("Leave blank to Keep current value.")

        new_name = self.get_feedback("New name: ") or None
        new_railway_id = self.get_feedback("New rialway ID: ") or None

        average_velocity = self.get_feedback("New average velocity: ")
        new_average_velocity = float(average_velocity) if average_velocity else None

        stop_time = self.get_feedback("New stop time: ")
        new_stop_time = float(stop_time) if stop_time else None

        quality_index = self.get_feedback("New quality index: ")
        new_quality_index = float(quality_index) if quality_index else None

        ticket_price = self.get_feedback("New ticket_price: ")
        new_ticket_price = float(ticket_price) if ticket_price else None

        capacity = self.get_feedback("New capacity: ")
        new_capacity = int(capacity) if capacity else None

        result = controller.services.staff.update_train(
            name,
            new_name,
            new_railway_id,
            new_average_velocity,
            new_quality_index,
            new_ticket_price,
            new_stop_time,
            new_capacity,
        )
        print(result.message)
        self.pause()

    def list_trains(self, controller: MenuController) -> None:
        self.show_title("Train List")

        result = controller.services.staff.get_all_trains()

        if not result.data:
            print("No train found.")
            self.pause()
            return

        for train in result.data:
            print(train)

        self.pause()
