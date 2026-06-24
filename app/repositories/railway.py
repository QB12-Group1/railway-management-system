from app.models.railway import Railway
from app.repositories.base import Repository

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

    def modify_by_name(
        self,
        name: str,
        length: float | None = None,
        start_station: str | None = None,
        end_station: str | None = None,
    ) -> bool:
        railway = self.get_by_name(name)
        if railway is None:
            return False
        if length is not None:
            railway.length = length
        if start_station is not None:
            railway.start_station = start_station
        if end_station is not None:
            railway.end_station = end_station
        return True
    
