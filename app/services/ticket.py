import time

from app.models.railway import Railway
from app.models.ticket import Ticket
from app.models.train import Train
from app.models.transaction import Transaction, TransactionType
from app.models.user import Customer
from app.repositories.railway import RailwayRepository
from app.repositories.ticket import TicketRepository
from app.repositories.train import TrainRepository
from app.repositories.transaction import TransactionRepository
from app.repositories.user import UserRepository
from app.services.base import Service, ServiceResult


class TicketService(Service):
    """
    Service for managing ticket purchases, exports, and train availability.

    This service handles the core logic for users buying tickets,
    exporting ticket data to a file, and retrieving a list of trains
    that still have available capacity.
    """

    def __init__(
        self,
        ticket_repository: TicketRepository,
        train_repository: TrainRepository,
        user_repository: UserRepository,
        railway_repository: RailwayRepository,
        transaction_repository: TransactionRepository,
    ) -> None:
        """
        Initializes the TicketService with necessary repositories.

        Args:
            ticket_repository: Repository for accessing ticket data.
            train_repository: Repository for accessing train data.
            user_repository: Repository for accessing user data.
            railway_repository: Repository for accessing railway data.
        """
        self.ticket_repository = ticket_repository
        self.train_repository = train_repository
        self.user_repository = user_repository
        self.railway_repository = railway_repository
        self.transaction_repository = transaction_repository

    def buy_ticket(
        self, customer_id: str, train_name: str, destination_station: str, quantity=1
    ) -> ServiceResult[list[Ticket]]:
        """
        Handles the process of a customer buying one or more tickets for a train.

        Performs validation checks including:
        - Customer existence and type.
        - Train existence and railway assignment.
        - Railway existence.
        - Destination station being on the train's route.
        - Ticket quantity being valid.
        - Sufficient train capacity.
        - Sufficient customer wallet balance.

        If all checks pass, it deducts the cost from the customer's wallet,
        reduces the train's capacity, creates the ticket(s), and saves them.

        Args:
            customer_id: The unique identifier of the customer purchasing tickets.
            train_name: The name of the train for which tickets are being purchased.
            destination_station: The name of the final station for the ticket.
            quantity: The number of tickets to purchase (default is 1).

        Returns:
            A ServiceResult indicating success with the list of purchased tickets,
            or failure with an appropriate error message.
        """
        customer = self.user_repository.get_by_id(customer_id)

        if customer is None or not isinstance(customer, Customer):
            return self.failure(f"Customer with ID '{customer_id}' was not found.")

        train = self.train_repository.get_by_name(train_name)
        if train is None:
            return self.failure(f"Train '{train_name}' does not exist.")

        if train.railway_id is None:
            return self.failure(
                f"Train '{train_name}' is currently not assigned to any railway."
            )

        railway = self.railway_repository.get_by_id(train.railway_id)
        if railway is None:
            return self.failure("The railway assigned to this train no longer exists.")

        # Check if the station exists on this route
        if destination_station not in railway.all_stations:
            return self.failure(
                f"Station '{destination_station}' is not on the '{railway.name}' route."
            )

        if quantity <= 0:
            return self.failure("Ticket quantity must be at least 1.")

        if train.capacity < quantity:
            return self.failure(
                f"Not enough capacity. Only {train.capacity} seats remaining."
            )

        total_cost = train.ticket_price * quantity
        if total_cost > customer.wallet.balance:
            return self.failure(
                f"Insufficient balance. Required: {total_cost}, Available: {customer.wallet.balance}"
            )

        # Process transaction
        customer.wallet.balance -= total_cost
        train.capacity -= quantity  # Decrease train capacity upon purchase

        fmt_time = time.strftime("%Y-%m-%d | %H:%M:%S", time.localtime())

        tickets = [
            Ticket(
                ticket_price=train.ticket_price,
                train_id=train.id,
                customer_id=customer.id,
                destination_station=destination_station,
                purchase_time=fmt_time,
            )
            for _ in range(quantity)
        ]
        self.ticket_repository.add_many(tickets)

        self.transaction_repository.add(
            Transaction(
                customer_id=customer_id,
                amount=-total_cost,
                transaction_type=TransactionType.PURCHASE,
                balance_after=customer.wallet.balance,
                t=fmt_time,
            )
        )
        try:
            self.transaction_repository.export_customer_transactions(
                customer_id=customer_id, username=customer.username
            )
        except Exception as e:
            return self.failure(
                f"An unexpected error occurred during ticket export: {str(e)}"
            )

        return self.success(
            f"Successfully purchased {quantity} ticket(s) for train '{train_name}'.",
            tickets,
        )

    def export_tickets_to_file(self, file_path: str) -> ServiceResult[None]:
        """
        Exports all existing tickets to a specified file.

        Each line in the file will contain details about a ticket, including
        customer name, destination, train information, and price.

        Args:
            file_path: The path to the file where tickets should be exported.

        Returns:
            A ServiceResult indicating success or failure of the export operation.
            If a ticket references a non-existent customer or train, it will be
            skipped in the export, but the operation will still be considered successful
            if other tickets are exported.
        """
        tickets = self.ticket_repository.get_all()

        if not tickets:
            return self.failure("No tickets found in the system to export.")

        try:
            with open(file_path, mode="w") as file:
                for ticket in tickets:
                    train = self.train_repository.get_by_id(ticket.train_id)
                    customer = self.user_repository.get_by_id(ticket.customer_id)

                    if customer is None or not isinstance(customer, Customer):
                        continue

                    if train is None:
                        train_name = "Unknown Train"
                        train_id = ticket.train_id
                    else:
                        train_name = train.name
                        train_id = train.id

                    file.write(
                        f"Ticket ID: {ticket.id} | "
                        f"Purchase Time: {ticket.purchase_time} | "
                        f"Customer: {customer.full_name} (ID: {customer.id}) | Destination: {ticket.destination_station} | "
                        f"Train: {train_name} (ID: {train_id}) | Price: {ticket.ticket_price}\n"
                    )
            return self.success(f"Tickets successfully exported to {file_path}.")
        except Exception as e:
            return self.failure(
                f"An unexpected error occurred during ticket export: {str(e)}"
            )

    def get_available_trains(self) -> ServiceResult[list[tuple[Railway, Train]]]:
        """
        Retrieves a list of available trains paired with their railway.

        Only trains with available capacity and an assigned railway are included.

        Returns:
            A ServiceResult containing a list of (Railway, Train) tuples,
            or a failure message if no available trains are found.
        """

        all_trains = self.train_repository.get_all()
        available_trains = []
        for train in all_trains:
            if train.capacity <= 0:
                continue
            if train.railway_id is None:
                continue
            railway = self.railway_repository.get_by_id(train.railway_id)
            if railway is None:
                continue

            available_trains.append((railway, train))

        if not available_trains:
            return self.failure("No available train found.")

        return self.success(
            f"Found {len(available_trains)} available train(s).", available_trains
        )

    def get_customer_tickets(
        self, customer: Customer
    ) -> ServiceResult[list[tuple[Ticket, Train]]]:
        """
        Retrieve all tickets purchased by a specific customer along with their trains.

        This method iterates through all stored tickets, selects those belonging to the
        provided customer, and pairs each ticket with its corresponding train. Only
        tickets whose associated train exists in the train repository are included.

        Args:
            customer (Customer): The customer whose purchased tickets should be retrieved.

        Returns:
            ServiceResult[list[tuple[Ticket, Train]]]:
                - Success: Contains a list of `(Ticket, Train)` tuples representing the
                customer's purchased tickets and their associated trains.
                - Failure: Returned if the customer has not purchased any tickets.
        """
        purchased_tickets: list[tuple[Ticket, Train]] = []

        for ticket in self.ticket_repository.get_all():
            if ticket.customer_id == customer.id:
                train = self.train_repository.get_by_id(ticket.train_id)
                if train is not None:
                    purchased_tickets.append((ticket, train))

        if not purchased_tickets:
            return self.failure("Customer has not purchased any tickets")

        return self.success(
            "Customer tickets retrieved successfully", purchased_tickets
        )
