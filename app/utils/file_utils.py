import os


def get_data_path(filename: str) -> str:
    """
    Ensures the 'data/' directory exists and returns a safe,
    sanitized path for the given filename inside that directory.
    """
    target_dir = "data"
    os.makedirs(target_dir, exist_ok=True)
    sanitized_filename = os.path.basename(filename)
    return os.path.join(target_dir, sanitized_filename)
