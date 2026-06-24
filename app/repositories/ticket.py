from app.models.ticket import Ticket
from app.repositories.base import Repository


class TicketRepository(Repository[Ticket]):
    """
    Repository for managing tickets in the system.

    This repository extends the base Repository with ticket-specific
    query operations, allowing retrieval based on customers or trains.
    """

    def get_by_customer_id(self, customer_id: str) -> list[Ticket]:
        """
        Retrieve all tickets belonging to a specific customer.

        Args:
            customer_id (str): The unique identifier of the customer.

        Returns:
            list[Ticket]: A list of tickets associated with the customer.
        """
        tickets = []
        for ticket in self.items:
            if ticket.customer_id == customer_id:
                tickets.append(ticket)
        return tickets

    def get_by_train_name(self, train_id: str) -> list[Ticket]:
        """
        Retrieve all tickets issued for a specific train.

        Args:
            train_id (str): The unique identifier of the train.

        Returns:
            list[Ticket]: A list of tickets associated with the train.
        """
        tickets = []
        for ticket in self.items:
            if ticket.train_id == train_id:
                tickets.append(ticket)
        return tickets
