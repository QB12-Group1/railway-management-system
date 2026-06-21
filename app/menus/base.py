from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

"""Base menu abstraction."""


if TYPE_CHECKING:
    from app.menu_controller import MenuController


class BaseMenu(ABC):
    """Abstract base class for all menus."""

    @abstractmethod
    def display(self, controller: MenuController) -> None:
        """Render the menu and handle user interaction."""
        raise NotImplementedError
