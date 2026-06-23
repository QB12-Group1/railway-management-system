class Railway:
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
        self.name = name
        self.origin = origin
        self.destination = destination
        self.stations = stations
