import re

INVALID_PASSWORD_MESSAGE = "Password must contain at least one lowercase letter, one uppercase letter, one number, and either '@' or '&'."


def invalid_email_message(email: str) -> str:
    return f"Email '{email}' is not a valid email address."


def validate_email(email: str) -> bool:
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    match = re.match(pattern, email)
    return bool(match)


def validate_password(password: str) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@&])[A-Za-z\d@&]+$"
    match = re.match(pattern, password)
    return bool(match)
