class Ticket:
    def __init__(
        self, destination_station: str, train_name: str, ticket_price: int
    ) -> None:
        self.destination_station = destination_station
        self.train_name = train_name
        self.ticket_price = ticket_price
