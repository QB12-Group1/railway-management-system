from __future__ import annotations

from dataclasses import dataclass

from app.services.admin import AdminService
from app.services.auth import AuthenticationService
from app.services.customer import CustomerService
from app.services.staff import StaffService
from app.services.ticket import TicketService
from app.services.wallet import WalletService


@dataclass(frozen=True)
class ServiceContext:
    """Application services shared across menus."""

    auth: AuthenticationService
    customer: CustomerService
    wallet: WalletService
    staff: StaffService
    admin: AdminService
    ticket: TicketService
