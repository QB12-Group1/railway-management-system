from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

"""Base menu abstraction."""


if TYPE_CHECKING:
    from app.menu_controller import MenuController


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

    @abstractmethod
    def display(self, controller: MenuController) -> None:
        """Render the menu and handle user interaction."""
        raise NotImplementedError
