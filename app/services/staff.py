from app.models.railway import Railway
from app.models.train import Train
from app.repositories.railway import RailwayRepository
from app.repositories.train import TrainRepository
from app.services.base import Service, ServiceResult


class StaffService(Service):
    """
    Service responsible for administrative operations related to transport infrastructure.

    This service allows staff members to manage railways and trains, providing
    functionality for adding, removing, updating, and retrieving these entities
    while ensuring business logic validation.
    """

    def __init__(
        self, railway_repository: RailwayRepository, train_repository: TrainRepository
    ) -> None:
        """
        Initialize the StaffService.

        Args:
            railway_repository (RailwayRepository): The repository for railway data.
            train_repository (TrainRepository): The repository for train data.
        """
        self.railway_repository = railway_repository
        self.train_repository = train_repository

    def add_railway(
        self, name: str, origin: str, destination: str, stations: list[str]
    ) -> ServiceResult[Railway]:
        """
        Register a new railway route in the system.

        Args:
            name (str): Unique name of the railway.
            origin (str): Starting station name.
            destination (str): Ending station name.
            stations (list[str]): List of stations included in the route.

        Returns:
            ServiceResult[Railway]: A success result containing the newly
            created Railway instance, or a failure result.
        """
        if self.railway_repository.exists_by_name(name):
            return self.failure(f"A railway named '{name}' already exists.")

        result = self._validate_route(origin, destination, stations)
        if not result.success:
            return self.failure(result.message)

        railway = Railway(name, origin, destination, stations)
        self.railway_repository.add(railway)
        return self.success(
            f"Railway '{name}' has been registered successfully.", railway
        )

    def remove_railway(self, name: str) -> ServiceResult[None]:
        """
        Remove a railway from the system and detach associated trains.

        Args:
            name (str): The name of the railway to remove.

        Returns:
            ServiceResult[None]: Success message if removed, otherwise failure.
        """
        result = self._get_railway_or_failure(name)
        if result.data is None:
            return self.failure(result.message)

        operating_trains = self.train_repository.get_all_by_railway_id(result.data.id)
        for train in operating_trains:
            train.railway_id = None

        self.railway_repository.remove(result.data)
        return self.success(f"Railway '{name}' has been removed successfully.")

    def update_railway(
        self,
        name: str,
        new_name: str | None = None,
        new_origin: str | None = None,
        new_destination: str | None = None,
        new_stations: list[str] | None = None,
    ) -> ServiceResult[Railway]:
        """
        Update the details of an existing railway.

        Args:
            name (str): The current name of the railway.
            new_name (str | None): The new name, if renaming. Defaults to None.
            new_origin (str | None): The new origin station. Defaults to None.
            new_destination (str | None): The new destination station. Defaults to None.
            new_stations (list[str] | None): The new list of stations. Defaults to None.

        Returns:
            ServiceResult[Railway]: The updated Railway object on success,
            or a failure result.
        """
        result = self._get_railway_or_failure(name)
        if result.data is None:
            return result

        if new_name and new_name != name:
            if self.railway_repository.exists_by_name(new_name):
                return self.failure(
                    f"Cannot rename to '{new_name}' because that name is already in use."
                )

        railway = result.data
        origin = new_origin if new_origin is not None else railway.origin
        destination = (
            new_destination if new_destination is not None else railway.destination
        )
        stations = new_stations if new_stations is not None else railway.stations

        result = self._validate_route(origin, destination, stations)
        if not result.success:
            return self.failure(result.message)

        self.railway_repository.update_by_name(
            name, new_name, origin, destination, stations
        )
        return self.success(
            f"Railway '{new_name if new_name else name}' has been updated successfully.",
            railway,
        )

    def get_all_railways(self) -> ServiceResult[list[Railway]]:
        """
        Retrieve all registered railways.

        Returns:
            ServiceResult[list[Railway]]: Success result containing a list of all railways.
        """
        railways = self.railway_repository.get_all()
        return self.success("All railways have been retrieved.", railways)

    def add_train(
        self,
        name: str,
        railway_id: str,
        average_velocity: float,
        stop_time: float,
        quality_index: float,
        ticket_price: float,
        capacity: int,
    ) -> ServiceResult[Train]:
        """
        Register a new train in the system.

        Args:
            name (str): Unique name of the train.
            railway_id (str): ID of the railway it operates on.
            average_velocity (float): Average speed of the train.
            stop_time (float): Total stop time at stations.
            quality_index (float): Quality rating (0-10).
            ticket_price (float): Base price for a ticket.
            capacity (int): Total seat capacity.

        Returns:
            ServiceResult[Train]: A success result containing the newly
            created Train instance, or a failure result.
        """
        if self.train_repository.exists_by_name(name):
            return self.failure(f"A train named '{name}' already exists.")

        if not self.railway_repository.exists_by_id(railway_id):
            return self.failure(f"No railway found with the ID '{railway_id}'.")

        result = self._validate_positive(average_velocity, "Average velocity")
        if not result.success:
            return self.failure(result.message)

        result = self._validate_quality_index(quality_index)
        if not result.success:
            return self.failure(result.message)

        result = self._validate_positive(ticket_price, "Ticket price")
        if not result.success:
            return self.failure(result.message)

        result = self._validate_positive(capacity, "Capacity")
        if not result.success:
            return self.failure(result.message)

        train = Train(
            name,
            railway_id,
            average_velocity,
            stop_time,
            quality_index,
            ticket_price,
            capacity,
        )
        self.train_repository.add(train)
        return self.success(f"Train '{name}' has been registered successfully.", train)

    def remove_train(self, name: str) -> ServiceResult[None]:
        """
        Remove a train from the system.

        Args:
            name (str): The name of the train to remove.

        Returns:
            ServiceResult[None]: Success message if removed, otherwise failure.
        """
        result = self._get_train_or_failure(name)
        if result.data is None:
            return self.failure(result.message)

        self.train_repository.remove(result.data)
        return self.success(f"Train '{name}' has been removed successfully.")

    def update_train(
        self,
        name,
        new_name: str | None = None,
        new_railway_id: str | None = None,
        new_average_velocity: float | None = None,
        new_stop_time: float | None = None,
        new_quality_index: float | None = None,
        new_ticket_price: float | None = None,
        new_capacity: int | None = None,
    ) -> ServiceResult[Train]:
        """
        Update the attributes of an existing train.

        Args:
            name (str): The current name of the train.
            new_name (str | None): The new name, if renaming. Defaults to None.
            new_railway_id (str | None): New railway ID. Defaults to None.
            new_average_velocity (float | None): New average velocity. Defaults to None.
            new_stop_time (float | None): New stop time. Defaults to None.
            new_quality_index (float | None): New quality index. Defaults to None.
            new_ticket_price (float | None): New ticket price. Defaults to None.
            new_capacity (int | None): New capacity. Defaults to None.

        Returns:
            ServiceResult[Train]: The updated Train object on success,
            or a failure result.
        """
        result = self._get_train_or_failure(name)
        if not result.data:
            return result

        if new_name and new_name != name:
            if not self.train_repository.exists_by_name(new_name):
                return self.failure(
                    f"Cannot rename to '{new_name}' because that name is already in use."
                )

        train = result.data
        if new_railway_id and new_railway_id != train.railway_id:
            if not self.railway_repository.exists_by_id(new_railway_id):
                return self.failure(f"No railway found with the ID '{new_railway_id}'.")

        self.train_repository.update_by_name(
            name,
            new_name,
            new_railway_id,
            new_average_velocity,
            new_stop_time,
            new_quality_index,
            new_ticket_price,
            new_capacity,
        )
        return self.success(
            f"Train '{new_name if new_name else name}' has been updated successfully.",
            train,
        )

    def get_all_trains(self) -> ServiceResult[list[Train]]:
        """
        Retrieve all registered trains.

        Returns:
            ServiceResult[list[Train]]: Success result containing a list of all trains.
        """
        trains = self.train_repository.get_all()
        return self.success("All trains have been retrieved.", trains)

    def _validate_positive(
        self, value: float | int, field_name: str
    ) -> ServiceResult[None]:
        """
        Check if a numeric value is greater than zero.

        Args:
            value (float | int): The value to validate.
            field_name (str): The name of the field for error reporting.

        Returns:
            ServiceResult[None]: Success result if positive, otherwise failure.
        """
        if value <= 0:
            return self.failure(f"{field_name} must be greater than zero.")
        return self.success(f"{field_name} is valid.")

    def _validate_quality_index(self, quality_index: float) -> ServiceResult[None]:
        """
        Validate that the quality index is within the allowed range (0-10).

        Args:
            quality_index (float): The quality index to validate.

        Returns:
            ServiceResult[None]: Success result if valid, otherwise failure.
        """
        if not (0 <= quality_index <= 10):
            return self.failure("Quality index must be between 0 and 10.")
        return self.success("Quality index is valid.")

    # TODO: implement a better validation (cheking if the origin and stations aren't included in the stations list)
    def _validate_route(
        self, origin: str, destination: str, stations: list[str]
    ) -> ServiceResult[None]:
        """
        Validate the consistency of a railway route.

        Args:
            origin (str): Origin station.
            destination (str): Destination station.
            stations (list[str]): List of stations.

        Returns:
            ServiceResult[None]: Success result if valid, otherwise failure.
        """
        if origin == destination:
            return self.failure("The origin and destination cannot be the same.")
        if not stations:
            return self.failure(
                "A railway must include at least one station to define a route."
            )
        return self.success("The route is valid.")

    def _get_railway_or_failure(self, name: str) -> ServiceResult[Railway]:
        """
        Retrieve a railway by name or return a failure result.

        Args:
            name (str): The name of the railway.

        Returns:
            ServiceResult[Railway]: The Railway object or failure if not found.
        """
        railway = self.railway_repository.get_by_name(name)
        if railway is None:
            return self.failure(f"No railway found with the name '{name}'.")
        return self.success(f"Railway '{name}' found.", railway)

    def _get_train_or_failure(self, name: str) -> ServiceResult[Train]:
        """
        Retrieve a train by name or return a failure result.

        Args:
            name (str): The name of the train.

        Returns:
            ServiceResult[Train]: The Train object or failure if not found.
        """
        train = self.train_repository.get_by_name(name)
        if train is None:
            return self.failure(f"No train found with the name '{name}'.")

        return self.success(f"Train '{name}' found.", train)
