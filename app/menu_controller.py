from __future__ import annotations

from typing import TYPE_CHECKING

from app.context import ServiceContext

"""Stack-based menu controller."""

if TYPE_CHECKING:
    from app.menus.base import BaseMenu


class MenuController:
    """Controls menu navigation using a stack."""

    def __init__(self, services: ServiceContext) -> None:
        self._stack: list[BaseMenu] = []
        self.services = services

    def push(self, menu: BaseMenu) -> None:
        """Push a new menu onto the stack."""
        self._stack.append(menu)

    def pop(self) -> None:
        """Remove the current menu from the stack."""
        if self._stack:
            self._stack.pop()

    def current(self) -> BaseMenu | None:
        """Return the current menu."""
        return self._stack[-1] if self._stack else None

    def run(self) -> None:
        """Run the main event loop until the stack is empty."""
        while self._stack:
            menu = self.current()
            if menu is None:
                break
            menu.display(self)
