from app.models.base import Model


class Train(Model):
    """
    Represents a train available for booking in the railway system.

    A train has operational characteristics such as its average velocity,
    stop time, service quality, ticket price, and passenger capacity.
    The class also provides a method to book a seat on the train.

    Args:
        name (str): The name or identifier of the train.
        railway_id (str | None): The unique identifier of the railway operating the train,
            or None if the train is currently unassigned.
        average_velocity (float): The train's average travel speed.
        stop_time (float): The average stop duration at stations.
        quality_index (float): A numerical score representing the quality or comfort level of the train service.
        ticket_price (float): Price of a single ticket for this train.
        capacity (int): The total number of available seats on the train.

    Attributes:
        name (str): The train's name.
        railway_id (str | None): The unique identifier for the railway operator.
            Can be None if the railway has been deleted or the train is not in service.
        average_velocity (float): Average travel speed of the train.
        stop_time (float): Average stop duration at stations.
        quality_index (float): Quality rating of the train service.
        ticket_price (float): Cost of a ticket for this train.
        capacity (int): Remaining number of available seats.
    """

    def __init__(
        self,
        name: str,
        railway_id: str | None,
        average_velocity: float,
        stop_time: float,
        quality_index: float,
        ticket_price: float,
        capacity: int,
    ) -> None:
        super().__init__()
        self.name = name
        self.railway_id = railway_id
        self.average_velocity = average_velocity
        self.stop_time = stop_time
        self.quality_index = quality_index
        self.ticket_price = ticket_price
        self.capacity = capacity

    def book(self) -> None:
        """
        Reserve a seat on the train.

        Decreases the available capacity by one. If no seats remain,
        a ValueError is raised.

        Raises:
            ValueError: If there are no available seats to book.
        """
        if self.capacity <= 0:
            raise ValueError("No seats available.")
        self.capacity -= 1
