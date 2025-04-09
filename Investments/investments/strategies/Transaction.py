class Transaction:
    def __init__(self, transaction_open, transaction_amount):
        self.date_open = transaction_open
        self.date_closed = None
        self.returned = False
        self.funds = transaction_amount

    def close(self, date_closed):
        self.date_open = date_closed

        if self.funds >