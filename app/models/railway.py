from app.models.base import Model


class Railway(Model):
    """
    Represents a railway line with a name, origin, destination, and intermediate stations.

    Attributes:
        name (str): The name of the railway line.
        origin (str): The starting station of the railway line.
        destination (str): The final station of the railway line.
        stations (list[str]): Ordered list of stations between the origin and destination.
    """

    def __init__(
        self, name: str, origin: str, destination: str, stations: list[str]
    ) -> None:
        """
        Initialize a Railway instance.

        Args:
            name (str): The name of the railway line.
            origin (str): The starting station.
            destination (str): The ending station.
            stations (list[str]): List of intermediate stations on the route.
        """
        super().__init__()
        self.name = name
        self.origin = origin
        self.destination = destination
        self.stations = stations

    @property
    def all_stations(self) -> list[str]:
        return [self.origin] + self.stations + [self.destination]

    @property
    def route(self) -> str:
        return " -> ".join(self.all_stations)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.name}]: {self.route}"
