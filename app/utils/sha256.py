import hashlib
import os


def hash_password(password: str) -> str:
    """Hash a password with a randomly generated salt.

    This function creates a 16-byte random salt, converts it to a
    hexadecimal string, and prepends it to the password before computing
    a SHA-256 hash. The returned value stores both the salt and the hash
    separated by a dollar sign.

    Args:
        password: The plain-text password to hash.

    Returns:
        A string containing the salt and hashed password in the format ``"<salt>$<hash>"``.
    """
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(password: str, stored: str) -> bool:
    """Verify a plain-text password against a stored salted hash.

    This function extracts the salt and hash from the stored password
    string, recomputes the SHA-256 hash using the provided password and
    extracted salt, and compares the result to the stored hash.

    Args:
        password: The plain-text password to verify.
        stored: The stored salted hash in the format ``"<salt>$<hash>"``.

    Returns:
        ``True`` if the password matches the stored hash, otherwise ``False``.
    """
    salt, hashed = stored.split("$")
    check_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return check_hash == hashed
