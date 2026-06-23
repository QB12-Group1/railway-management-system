from app.models.railway import Railway
from app.repositories.base import Repository


class RailwayRepository(Repository[Railway]):
   

    def __init__(self) -> None:
       
        super().__init__()

    def add(self, item: Railway) -> None:
       
        super().add(item)

    def remove(self, item: Railway) -> bool:
      
        return super().remove(item)

    def update(self, item: Railway) -> bool:
        
        return super().update(item)

    def get_all(self) -> list[Railway]:
        
        return super().get_all()


