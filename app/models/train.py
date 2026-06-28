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
        capacity (int): The current number of available seats on the train.
        max_capacity (int): The original total capacity of the train.

    Attributes:
        name (str): The train's name.
        railway_id (str | None): The unique identifier for the railway operator.
            Can be None if the railway has been deleted or the train is not in service.
        average_velocity (float): Average travel speed of the train.
        stop_time (float): Average stop duration at stations.
        quality_index (float): Quality rating of the train service.
        ticket_price (float): Cost of a ticket for this train.
        capacity (int): The initial total number of seats available.
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
        self.max_capacity = capacity

    @property
    def average_velocity(self) -> float:
        return self._average_velocity

    @average_velocity.setter
    def average_velocity(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Average velocity must be greater than zero")
        self._average_velocity = value

    @property
    def stop_time(self) -> float:
        return self._stop_time

    @stop_time.setter
    def stop_time(self, value: float) -> None:
        if value < 0:
            raise ValueError("Stop time cannot be negative")
        self._stop_time = value

    @property
    def quality_index(self) -> float:
        return self._quality_index

    @quality_index.setter
    def quality_index(self, value: float) -> None:
        if not (0 <= value <= 10):
            raise ValueError("Quality index must be between 0 and 10")
        self._quality_index = value

    @property
    def ticket_price(self) -> float:
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Ticket price must be greater than zero")
        self._ticket_price = value

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        if value < 0:
            raise ValueError("capacity cannot be negative")

        if hasattr(self, "_max_capacity") and value > self.max_capacity:
            raise ValueError("Capacity cannot exceed max capacity")

        self._capacity = value

    @property
    def max_capacity(self) -> int:
        return self._max_capacity

    @max_capacity.setter
    def max_capacity(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Max capacity must be greater than zero")
        self._max_capacity = value

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

    def __str__(self) -> str:
        """
        Returns a concise representation of the train: Class[Name]: Status (Availability).
        """
        railway = self.railway_id or "N/A"
        return (
            f"{self.__class__.__name__}[{self.name}]: "
            f"{self.capacity}/{self.max_capacity} seats | "
            f"price = {self.ticket_price:.2f} | "
            f"speed = {self.average_velocity:.1f} km/h | "
            f"stop = {self.stop_time:.1f} min | "
            f"quality = {self.quality_index:.1f} | "
            f"railway = {railway}"
        )
