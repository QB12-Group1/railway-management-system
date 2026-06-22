class Train:
    def __init__(
        self,
        id: int,
        name: str,
        associatedRailway: str,
        averageVelocity: float,
        stopTime: float,
        qualityIndex: float,
        ticketPrice: float,
        capacity: int,
    ):
        self.id = id
        self.name = name
        self.associatedRailway = associatedRailway
        self.averageVelocity = averageVelocity
        self.stopTime = stopTime
        self.qualityIndex = qualityIndex
        self.ticketPrice = ticketPrice
        self.capacity = capacity

    def purchase_ticket(self):
        if self.capacity <= 0:
            raise ValueError("NO seats available.")
        self.capacity -= 1
