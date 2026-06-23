import uuid


def generate_id() -> str:
    """
    Generate a unique identifier using UUID4.

    This function creates a random UUID (version 4) and returns it as
    a string. UUID4 values are generated using random numbers, making
    them suitable for unique identifiers in most applications.

    The returned value is a string representation of the UUID.

    Returns:
        str: A randomly generated UUID4 string (e.g., "3f9c2f1e-7c2b-4b5f-a0a4-9f8d2e6a1cbb").
    """
    id = uuid.uuid4()
    return str(id)
