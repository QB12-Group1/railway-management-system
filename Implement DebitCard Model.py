class DebitCard:
    def __init__(self, card_number, expiration_month, expiration_year, password, cvv2):
        self.card_number = card_number
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.password = password
        self.cvv2 = cvv2

    @property
    def card_number(self):
        return self._card_number

    @card_number.setter
    def card_number(self, value):
        if not (str(value).isdigit() and len(str(value)) == 16):
            raise ValueError("card_number باید دقیقاً ۱۶ رقم عددی باشد.")
        self._card_number = value

    @property
    def expiration_month(self):
        return self._expiration_month

    @expiration_month.setter
    def expiration_month(self, value):
        if not (isinstance(value, int) and 1 <= value <= 12):
            raise ValueError("expiration_month")
        self._expiration_month = value

    @property
    def expiration_year(self):
        return self._expiration_year

    @expiration_year.setter
    def expiration_year(self, value):
        if not (isinstance(value, int) and 1403 <= value <= 1408):
            raise ValueError("expiration_year")
        self._expiration_year = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not (str(value).isdigit() and len(str(value)) == 6):
            raise ValueError("password")
        self._password = value

    @property
    def cvv2(self):
        return self._cvv2

    @cvv2.setter
    def cvv2(self, value):
        if not (str(value).isdigit() and len(str(value)) == 3):
            raise ValueError("cvv2")
        self._cvv2 = value