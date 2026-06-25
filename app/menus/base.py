from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING

"""Base menu abstraction."""


if TYPE_CHECKING:
    from app.menu_controller import MenuController

MenuAction = Callable[["MenuController"], None]
"""Callable type used by menu options to receive and update the controller."""


class BaseMenu(ABC):
    """Abstract base class for all menus."""

    def show_title(self, title: str) -> None:
        print(f"=== {title} ===")

    def show_options(self, options: list[str]) -> None:
        for i, option in enumerate(options):
            print(f"[{i + 1}] {option}\n")

    def get_feedback(self, prompt: str = "Enter an option: ") -> str:
        return input(prompt).strip()

    def invalid_input(self) -> None:
        print("Invalid input! try again...")

    def pause(self, prompt: str = "Press Enter to continue...") -> None:
        """Wait for the user before continuing to the next menu render."""
        input(prompt)

    def get_required_feedback(self, prompt: str) -> str:
        """Prompt until the user enters a non-empty value."""
        while True:
            value = self.get_feedback(prompt)
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
        try:
            action = list(options.values())[int(choice) - 1]
        except (ValueError, IndexError):
            self.invalid_input()
            return

        action(controller)

    @abstractmethod
    def display(self, controller: MenuController) -> None:
        """Render the menu and handle user interaction."""
        raise NotImplementedError
