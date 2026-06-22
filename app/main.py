from __future__ import annotations

from app.menu_controller import MenuController
from app.menus.main_menu import MainMenu

"""Application entry point."""

# something


def main() -> None:
    """Create controller and start the application."""
    controller = MenuController()
    controller.push(MainMenu())
    controller.run()


if __name__ == "__main__":
    main()
