from app.models.railway import Railway
from app.repositories.base import Repository

'''first'''
class RailwayRepository(Repository[Railway]):

    def get_by_name(self, name: str) -> Railway | None:
        for railway in self.items:
            if railway.name == name:
                return railway
        return None

    def exists_by_name(self, name: str) -> bool:
        return self.get_by_name(name) is not None

    def remove_by_name(self, name: str) -> bool:
        railway = self.get_by_name(name)
        if railway is None:
            return False
        self.remove(railway)
        return True

    def update_by_name(
        self,
        name: str,
        origin: str | None = None,
        destination: str | None = None,
        stations: list[str] | None = None,
    ) -> bool:
        railway = self.get_by_name(name)
        if railway is None:
            return False
        if origin is not None:
            railway.origin = origin
        if destination is not None:
            railway.destination = destination
        if stations is not None:
            railway.stations = stations
        return True
    