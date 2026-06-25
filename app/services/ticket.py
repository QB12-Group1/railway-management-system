import time

from app.models.ticket import Ticket
from app.models.train import Train
from app.models.user import Customer
from app.repositories.railway import RailwayRepository
from app.repositories.ticket import TicketRepository
from app.repositories.train import TrainRepository
from app.repositories.user import UserRepository
from app.services.base import Service, ServiceResult


class TicketService(Service):
    # this train is object from Train class
    # this ticket is object from Ticket class

    def __init__(
        self,
        ticket_repository: TicketRepository,
        train_repository: TrainRepository,
        user_repository: UserRepository,
        railway_repository: RailwayRepository,
    ) -> None:
        self.ticket_repositoy = ticket_repository
        self.train_repository = train_repository
        self.user_repository = user_repository
        self.railway_repository = railway_repository

    def buy_ticket(
        self, customer_id: str, train_name: str, destination_station: str, quantity=1
    ) -> ServiceResult[list[Ticket]]:
        tickets = []

        customer = self.user_repository.get_by_id(customer_id)

        if customer is None:
            return self.failure(f"User '{customer_id}' is not found.")

        if not isinstance(customer, Customer):
            return self.failure(f"Customer '{customer_id}' is not found.")

        train = self.train_repository.get_by_name(train_name)

        if train is None:
            return self.failure(f" Train '{train_name}' is not found.")

        if train.railway_id is None:
            return self.failure("next day")

        railway = self.railway_repository.get_by_id(train.railway_id)

        if railway is None:
            return self.failure("next day")

        stations = [railway.origin] + railway.stations + [railway.destination]

        if destination_station not in stations:
            return self.failure("next day")

        if train.capacity < quantity:
            return self.failure("Train is full.")

        if quantity <= 0:
            return self.failure("next day")

        if (train.ticket_price) * quantity > customer.wallet.balance:
            return self.failure("Your balance is not enough.")

        customer.wallet.balance -= (train.ticket_price) * quantity

        t = time.localtime()
        fmt_time = time.strftime("%Y-%m-%d | %H:%M:%S", t)

        tickets = [
            Ticket(
                ticket_price=train.ticket_price,
                train_id=train.id,
                customer_id=customer.id,
                destination_station=destination_station,
                time=fmt_time,
            )
            for _ in range(quantity)
        ]

        self.ticket_repositoy.add_many(tickets)

        return self.success("Buy ticket", tickets)

    def export_tickets_to_file(self, file_path: str) -> ServiceResult[None]:
        tickets = self.ticket_repositoy.get_all()

        if not tickets:
            return self.failure("Dont have")

        with open(file_path, mode="w") as file:
            for ticket in tickets:
                train = self.train_repository.get_by_id(ticket.train_id)
                customer = self.user_repository.get_by_id(ticket.customer_id)

                if customer is None:
                    return self.failure("User is not found.")

                if not isinstance(customer, Customer):
                    return self.failure("Customer is not found.")

                if train is None:
                    return self.failure("Dont have train")

                file.write(
                    f"cusmter_name:{customer.full_name}  , destination_station:{ticket.destination_station} , train_id:{train.id} , train_name:{train.name} , remaining_capacity:{train.max_capacity - train.capacity} , price:{ticket.ticket_price} \n"
                )
            return self.success("Done")

    def get_all_trian(self) -> ServiceResult[list[Train]]:
        result = []

        trains = self.train_repository.get_all()

        for train in trains:
            if train.capacity <= 0:
                return self.failure("Dont have train")
            result.append(train)
        return self.success("Trains_list", result)
