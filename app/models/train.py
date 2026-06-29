from datetime import time

from app.models.base import Model


class Train(Model):
    """
    Represents a train available for booking in the railway system.

    A train belongs to a railway and contains operational information such as
    its travel speed, station stop time, service quality,
    ticket price, passenger capacity, and scheduled departure time. The class
    is used to model trains that passengers can book seats on.

    Args:
        name (str): Unique name or identifier of the train.
        railway_id (str | None): Identifier of the railway operating the train. Can be None if the train is not currently assigned to a railway.
        average_velocity (float): Average travel speed of the train.
        stop_time (float): Total stop duration at stations during the journey.
        quality_index (float): Service quality rating (typically between 0 and 10).
        ticket_price (float): Price of a single ticket for this train.
        capacity (int): Total number of seats available on the train.
        start_time (time): Scheduled departure time of the train.

    Attributes:
        name (str): The train's unique name.
        railway_id (str | None): Identifier of the railway that operates the train.
        average_velocity (float): Average speed of the train during travel.
        stop_time (float): Total time spent stopped at stations.
        quality_index (float): Quality rating of the train service.
        ticket_price (float): Cost of a single passenger ticket.
        capacity (int): Current number of available seats remaining.
        max_capacity (int): Maximum seat capacity of the train.
        start_time (time): Scheduled departure time of the train.
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
        start_time: time,
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
        self.start_time = start_time

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
            f"departure_time = {self.start_time} | "
            f"railway = {railway}"
        )
