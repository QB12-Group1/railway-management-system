from app.models.train import Train
from app.repositories.base import Repository


class TrainRepository(Repository[Train]):
    def get_by_name(self, name: str) -> Train | None:
        for train in self.items:
            if train.name == name:
                return train
        return None

    def exists_by_name(self, name: str) -> bool:
        return self.get_by_name(name) is not None

    def remove_by_name(self, name: str) -> bool:
        train = self.get_by_name(name)

        if train is None:
            return False

        self.remove(train)
        return True

    def update_by_name(
        self,
        name: str,
        railway: str | None = None,
        average_velocity: float | None = None,
        stop_time: float | None = None,
        quality_index: float | None = None,
        ticket_price: float | None = None,
        capacity: int | None = None,
    ) -> bool:
        train = self.get_by_name(name)

        if train is None:
            return False

        if railway is not None:
            train.railway = railway
        if average_velocity is not None:
            train.average_velocity = average_velocity
        if stop_time is not None:
            train.stop_time = stop_time
        if quality_index is not None:
            train.quality_index = quality_index
        if ticket_price is not None:
            train.ticket_price = ticket_price
        if capacity is not None:
            train.capacity = capacity

        return True
