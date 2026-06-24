from app.models.ticket import Ticket
from app.repositories.base import Repository


class TicketRepo(Repository[Ticket]):
    def get_by_customer_id(self, customer_id: str):
        res = []

        for i in self.items:
            if i.customer_id == customer_id:
                res.append(i)

        return res

    def get_by_train_name(self, train_name: str):
        res = []

        for i in self.items:
            if i.train_name == train_name:
                res.append(i)

        return res
