from app.models.train import Train
from app.repositories.base import Repository


class TrainRepository(Repository[Train]):
    """
    Repository for managing trains in the system.

    This repository extends the base Repository with train-specific
    operations. Trains are primarily identified by their unique name.
    """

    def get_by_name(self, name: str) -> Train | None:
        """
        Retrieve a train by its unique name.

        Args:
            name (str): The name to search for.

        Returns:
            Train | None: The matching train if found, otherwise None.
        """
        for train in self.items:
            if train.name == name:
                return train
        return None

    def exists_by_name(self, name: str) -> bool:
        """
        Check whether a train with the given name exists.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if a train with the name exists, otherwise False.
        """
        return self.get_by_name(name) is not None

    def remove_by_name(self, name: str) -> bool:
        """
        Remove a train from the repository using its name.

        Args:
            name (str): The name of the train to remove.

        Returns:
            bool: True if the train was removed, otherwise False.
        """
        train = self.get_by_name(name)

        if train is None:
            return False
        self.remove(train)
        return True

    def modify_by_name(
        self,
        name: str,
        railway: str | None = None,
        average_velocity: float | None = None,
        stop_time: float | None = None,
        quality_index: float | None = None,
        ticket_price: float | None = None,
        capacity: int | None = None,
    ) -> bool:
        """
        Update an existing train using its name.

        Only the fields provided will be modified.

        Args:
            name (str): The name of the train to update.
            railway (str | None): New railway name, if provided. Defaults to None.
            average_velocity (float | None): New average velocity, if provided. Defaults to None.
            stop_time (float | None): New stop time, if provided. Defaults to None.
            quality_index (float | None): New quality index, if provided. Defaults to None.
            ticket_price (float | None): New ticket price, if provided. Defaults to None.
            capacity (int | None): New capacity, if provided. Defaults to None.

        Returns:
            bool: True if the train was updated, otherwise False.
        """
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
