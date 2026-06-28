from __future__ import annotations

from app.context import ServiceContext
from app.menu_controller import MenuController
from app.menus.main_menu import MainMenu
from app.repositories.railway import RailwayRepository
from app.repositories.ticket import TicketRepository
from app.repositories.train import TrainRepository
from app.repositories.transaction import TransactionRepository
from app.repositories.user import UserRepository
from app.services.admin import AdminService
from app.services.auth import AuthenticationService
from app.services.customer import CustomerService
from app.services.staff import StaffService
from app.services.ticket import TicketService
from app.services.wallet import WalletService

"""Application entry point."""


def main() -> None:
    """Create services, controller, and start the application."""
    user_repository = UserRepository()
    train_repository = TrainRepository()
    ticket_repository = TicketRepository()
    railway_repository = RailwayRepository()
    transaction_repository = TransactionRepository()

    auth_service = AuthenticationService(user_repository)
    auth_service.register_admin("admin", "admin")
    customer_service = CustomerService(user_repository)
    wallet_service = WalletService(user_repository, transaction_repository)
    staff_service = StaffService(railway_repository, train_repository)
    admin_service = AdminService(user_repository, auth_service)
    ticket_service = TicketService(
        ticket_repository,
        train_repository,
        user_repository,
        railway_repository,
    )

    services = ServiceContext(
        auth=auth_service,
        customer=customer_service,
        wallet=wallet_service,
        staff=staff_service,
        admin=admin_service,
        ticket=ticket_service,
    )

    controller = MenuController(services)
    controller.push(MainMenu())
    controller.run()


if __name__ == "__main__":
    main()
