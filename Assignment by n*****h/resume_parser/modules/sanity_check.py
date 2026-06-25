import os
from pathlib import Path

def validate_resume_file(filepath, allowed_extensions, max_size_mb):

    path = Path(filepath)

    # File exists
    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {filepath}")

    # Is file
    if not path.is_file(): raise ValueError(f"Not a file: {filepath}")

    # Extension check
    extension = path.suffix.lower()

    if extension not in allowed_extensions:
        raise ValueError(f"Unsupported file type: {extension}. Allowed: {sorted(allowed_extensions)}")

    # Size check
    file_size = os.path.getsize(filepath)
    max_bytes = max_size_mb * 1024 * 1024

    if file_size > max_bytes:
        raise ValueError(f"File exceeds size limit ({max_size_mb} MB)")

    # Read permission check
    if not os.access(filepath, os.R_OK):
        raise PermissionError(f"Cannot read file: {filepath}")

    return True