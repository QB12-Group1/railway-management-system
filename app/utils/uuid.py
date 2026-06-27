import uuid


def generate_id() -> str:
    """Generate a random Universally Unique Identifier (UUID).

    This function generates a random UUID (version 4) and returns
    its canonical 36-character string representation.

    Returns:
        A string representing the generated UUIDv4.
    """
    id = uuid.uuid4()
    return str(id)
