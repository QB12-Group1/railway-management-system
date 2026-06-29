from app.models.base import Model


class Railway(Model):
    """
    Represents a railway line with a name, origin, destination, and intermediate stations.

    Attributes:
        name (str): The name of the railway line.
        origin (str): The starting station of the railway line.
        destination (str): The final station of the railway line.
        stations (list[str]): Ordered list of stations between the origin and destination.
        travel_distance (int): Total distance of the railway in kilometers.

    """

    def __init__(
        self,
        name: str,
        origin: str,
        destination: str,
        stations: list[str],
        travel_distance: int,
    ) -> None:
        """
        Initialize a Railway instance.

        Args:
            name (str): The name of the railway line.
            origin (str): The starting station.
            destination (str): The ending station.
            stations (list[str]): List of intermediate stations on the route.
            travel_distance (int): Total distance of the railway in kilometers.
        """
        super().__init__()
        self.name = name
        self.origin = origin
        self.destination = destination
        self.stations = stations
        self.travel_distance = travel_distance

    @property
    def all_stations(self) -> list[str]:
        return [self.origin] + self.stations + [self.destination]

    @property
    def route(self) -> str:
        return " -> ".join(self.all_stations)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.name}]: {self.route} ({self.travel_distance})"

    @property
    def travel_distance(self) -> int:
        """
        Get the travel distance of the railway.

        Returns:
            int: Total travel distance of the railway.
        """
        return self._travel_distance

    @travel_distance.setter
    def travel_distance(self, value: int) -> None:
        """
        Set the travel distance of the railway.

        Args:
            value (int): Total travel distance.
        Raises:
             ValueError: If the distance is less than or equal to zero.
        """
        if value <= 0:
            raise ValueError("Travel distance must be greater than zero")
        self._travel_distance = value
