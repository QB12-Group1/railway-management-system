from app.models.ticket import Ticket
from app.models.train import Train
from app.models.wallet import Wallet
from app.services.base import Service


class TicketService(Service):
    # this train is object from Train class
    # this ticket is object from Ticket class

    def buy_ticket(self, train: Train, quantity, ticket: Ticket, wallet: Wallet):
        tickets = []
        if (train.capacity > 0) and ((train.ticket_price * quantity) < wallet.balance):
            wallet.balance -= train.ticket_price * quantity

            for n in quantity:
                tickets.append([ticket.customer_id, train.name, n])
                train.book()

        return tickets

    def export_tickets_to_file(self, ticket: Ticket, train: Train, file_path):
        with open(file_path, mode="w") as file:
            file.writelines(
                f"Customer_id : {ticket.customer_id} , Train_name : {train.name}"
            )
