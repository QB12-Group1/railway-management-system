from app.models.base import Model


class Ticket(Model):
    """
    Represents a train ticket with basic travel information.

    Attributes:
        destination_station (str): The name of the station where the passenger is traveling to.
        train_name (str): The name or identifier of the train for the journey.
        ticket_price (int): The price of the ticket, typically in the smallest currency unit
            or the standard currency used by the system.
    """

    def __init__(
        self,
        destination_station: str,
        train_name: str,
        ticket_price: int,
        customer_id: str,
    ) -> None:
        """
        Initialize a new Ticket instance.

        Args:
            destination_station (str): Destination station for the trip.
            train_name (str): Name or identifier of the train.
            ticket_price (int): Cost of the ticket.
        """
        super().__init__()
        self.destination_station = destination_station
        self.train_name = train_name
        self.ticket_price = ticket_price
        self.customer_id = customer_id
