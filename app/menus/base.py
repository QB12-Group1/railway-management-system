from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING

"""Base menu abstraction."""


if TYPE_CHECKING:
    from app.menu_controller import MenuController

MenuAction = Callable[["MenuController"], None]
"""Callable type used by menu options to receive and update the controller."""

CANCEL_COMMAND = ["exit", "cancel"]
"""Input command used to cancel the current menu operation."""


class BaseMenu(ABC):
    """Abstract base class for all menus."""

    def show_title(self, title: str) -> None:
        print(f"\n=== {title} ===")

    def show_options(self, options: list[str]) -> None:
        for i, option in enumerate(options):
            print(f"[{i + 1}] {option}")

    def get_feedback(self, prompt: str = "Enter an option: ") -> str:
        return input(prompt).strip()

    def invalid_input(self) -> None:
        print("Invalid input! try again...")

    def show_not_implemented(self, controller: MenuController) -> None:
        """Fallback action for unfinished menu items."""
        print("This feature is not implemented yet.")
        controller.pop()

    def cancel_operation(
        self, controller: MenuController, exit_menu: bool = False
    ) -> None:
        """Cancel the current operation and optionally pop the current menu."""
        print("Operation cancelled.")
        if exit_menu:
            controller.pop()

    def is_cancel_command(self, value: str) -> bool:
        """Return True when the user input requests cancelling the operation."""
        return value.lower() in CANCEL_COMMAND

    def pause(self, prompt: str = "Press Enter to continue...") -> None:
        """Wait for the user before continuing to the next menu render."""
        input(prompt)

    def get_required_feedback(self, prompt: str) -> str | None:
        """Prompt until the user enters a value or the cancel command."""
        while True:
            value = self.get_feedback(prompt)
            if self.is_cancel_command(value):
                return None
            if value:
                return value
            self.invalid_input()

    def handle_options(
        self,
        controller: MenuController,
        title: str,
        options: dict[str, MenuAction],
    ) -> None:
        """Render numbered options and execute the action selected by the user."""
        self.show_title(title)
        self.show_options(list(options))

        choice = self.get_feedback()
        if self.is_cancel_command(choice):
            self.cancel_operation(controller, exit_menu=True)
            return

        try:
            action = (
                list(options.values())[int(choice) - 1]
                if choice.isnumeric()
                else options[choice]
            )
        except (KeyError, ValueError, IndexError):
            self.invalid_input()
            return

        action(controller)

    @abstractmethod
    def display(self, controller: MenuController) -> None:
        """Render the menu and handle user interaction."""
        raise NotImplementedError
