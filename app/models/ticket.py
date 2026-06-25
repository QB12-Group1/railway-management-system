from app.models.base import Model


class Ticket(Model):
    """
    Represents a train ticket with basic travel information.

    Attributes:
        destination_station (str): The name of the station where the passenger is traveling to.
        train_id (str): The unique identifier of the train associated with the ticket.
        ticket_price (float): The price of the ticket, typically in the smallest currency unit
            or the standard currency used by the system.
        customer_id (str): The unique identifier of the user who purchased the ticket.
        purchase_time (str): The timestamp of when the ticket was issued.
    """

    def __init__(
        self,
        destination_station: str,
        train_id: str,
        ticket_price: float,
        customer_id: str,
        purchase_time: str,
    ) -> None:
        """
        Initialize a new Ticket instance.

        Args:
            destination_station (str): Destination station for the trip.
            train_id (str): Unique identifier of the train.
            ticket_price (float): Cost of the ticket.
            customer_id (str): The unique identifier of the user who purchased the ticket.
            time (str):set time
        """
        super().__init__()
        self.destination_station = destination_station
        self.train_id = train_id
        self.ticket_price = ticket_price
        self.customer_id = customer_id
        self.purchase_time = purchase_time
