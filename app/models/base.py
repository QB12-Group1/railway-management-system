from app.utils.uuid import generate_id


class Model:
    """
    Base model that provides a unique identifier for derived models.

    Attributes:
        id (str): A unique identifier automatically generated for the model instance.
    """

    def __init__(self) -> None:
        """
        Initialize the base model and assign a unique ID.
        """
        self.id = generate_id()
