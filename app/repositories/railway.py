from app.models.railway import Railway
from app.repositories.base import Repository


class RailwayRepository(Repository[Railway]):
    """
    Repository for managing railway routes in the system.

    This repository extends the base Repository with railway-specific
    operations. Railways are primarily identified by their unique name.
    """

    def get_by_name(self, name: str) -> Railway | None:
        """
        Retrieve a railway by its unique name.

        Args:
            name (str): The name of the railway to search for.

        Returns:
            Railway | None: The matching railway if found, otherwise None.
        """
        for railway in self.items:
            if railway.name == name:
                return railway

        return None

    def exists_by_name(self, name: str) -> bool:
        """
        Check whether a railway with the given name exists.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if a railway with the name exists, otherwise False.
        """
        return self.get_by_name(name) is not None

    def remove_by_name(self, name: str) -> bool:
        """
        Remove a railway from the repository using its name.

        Args:
            name (str): The name of the railway to remove.

        Returns:
            bool: True if the railway was removed, otherwise False.
        """
        railway = self.get_by_name(name)

        if railway is None:
            return False

        return self.remove(railway)

    def update_by_name(
        self,
        name: str,
        new_name: str | None = None,
        origin: str | None = None,
        destination: str | None = None,
        stations: list[str] | None = None,
    ) -> bool:
        """
        Update an existing railway using its name.

        Only the fields provided will be modified.

        Args:
            name (str): The name of the railway to update.
            origin (str | None): New origin station, if provided. Defaults to None.
            destination (str | None): New destination station, if provided. Defaults to None.
            stations (list[str] | None): New list of intermediate stations, if provided. Defaults to None.

        Returns:
            bool: True if the railway was updated, otherwise False.
        """
        railway = self.get_by_name(name)

        if railway is None:
            return False

        if new_name is not None:
            railway.name = new_name
        if origin is not None:
            railway.origin = origin
        if destination is not None:
            railway.destination = destination
        if stations is not None:
            railway.stations = stations

        return True
