from app.models.base import Model


class DebitCard(Model):
    """
    Represents a debit card with basic validation for its fields.

    This class stores debit card information and ensures that each attribute
    satisfies common formatting constraints through property setters.

    Attributes:
        card_number (str): A 16-digit numeric string representing the card number.
        expiration_month (int): Expiration month of the card (1–12).
        expiration_year (int): Expiration year of the card (restricted to 1403–1408).
        pin (str): A 6-digit numeric string representing the card PIN.
        cvv2 (str): A 3-digit numeric string representing the card CVV2 code.
    """

    def __init__(
        self,
        card_number: str,
        expiration_month: int,
        expiration_year: int,
        pin: str,
        cvv2: str,
    ) -> None:
        """
        Initialize a DebitCard instance.

        Args:
            card_number (str): A 16-digit card number.
            expiration_month (int): Card expiration month (1–12).
            expiration_year (int): Card expiration year (1403–1408).
            pin (str): A 6-digit card PIN.
            cvv2 (str): A 3-digit CVV2 security code.

        Raises:
            ValueError: If any of the provided values fail validation.
        """
        self.card_number = card_number
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.pin = pin
        self.cvv2 = cvv2

    @property
    def card_number(self) -> str:
        """
        Get the card number.

        Returns:
            str: The 16-digit card number.
        """
        return self._card_number

    @card_number.setter
    def card_number(self, value: str) -> None:
        """
        Set the card number.

        Args:
            value (str): A 16-digit numeric string.

        Raises:
            ValueError: If the card number is not exactly 16 digits.
        """
        if not value.isdigit() or len(value) != 16:
            raise ValueError("Card number must be exactly 16 digits.")

        self._card_number = value

    @property
    def expiration_month(self) -> int:
        """
        Get the expiration month.

        Returns:
            int: The expiration month (1–12).
        """
        return self._expiration_month

    @expiration_month.setter
    def expiration_month(self, value: int) -> None:
        """
        Set the expiration month.

        Args:
            value (int): Month number between 1 and 12.

        Raises:
            ValueError: If the month is outside the valid range.
        """
        if not 1 <= value <= 12:
            raise ValueError("Expiration month must be between 1 and 12.")

        self._expiration_month = value

    @property
    def expiration_year(self) -> int:
        """
        Get the expiration year.

        Returns:
            int: The expiration year.
        """
        return self._expiration_year

    @expiration_year.setter
    def expiration_year(self, value: int) -> None:
        """
        Set the expiration year.

        Args:
            value (int): Year between 1403 and 1408.

        Raises:
            ValueError: If the year is outside the valid range.
        """
        if not 1403 <= value <= 1408:
            raise ValueError("Expiration year must be between 1403 and 1408.")

        self._expiration_year = value

    @property
    def pin(self) -> str:
        """
        Get the card PIN.

        Returns:
            str: The 6-digit PIN code.
        """
        return self._pin

    @pin.setter
    def pin(self, value: str) -> None:
        """
        Set the card PIN.

        Args:
            value (str): A 6-digit numeric string.

        Raises:
            ValueError: If the PIN is not exactly 6 digits.
        """
        if not value.isdigit() or len(value) != 6:
            raise ValueError("PIN must be exactly 6 digits.")

        self._pin = value

    @property
    def cvv2(self) -> str:
        """
        Get the CVV2 code.

        Returns:
            str: The 3-digit CVV2 code.
        """
        return self._cvv2

    @cvv2.setter
    def cvv2(self, value: str) -> None:
        """
        Set the CVV2 code.

        Args:
            value (str): A 3-digit numeric string.

        Raises:
            ValueError: If the CVV2 is not exactly 3 digits.
        """
        if not value.isdigit() or len(value) != 3:
            raise ValueError("CVV2 must be exactly 3 digits.")

        self._cvv2 = value
