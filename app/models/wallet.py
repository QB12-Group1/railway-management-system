class Wallet:
    def __init__(self, balance: float = 0.0, linkedCard=None):
        self.balance = balance
        self.linkedCard = linkedCard
