class Railway:
    def __init__(
        self, name: str, origin: str, destination: str, stations: list[str]
    ) -> None:
        self.name = name
        self.origin = origin
        self.destination = destination
        self.stations = stations
