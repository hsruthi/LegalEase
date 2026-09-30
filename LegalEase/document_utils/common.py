from pathlib import Path
from datetime import datetime


def ensure_output_directory(directory="generated_documents"):
    """Create the output directory if it does not exist."""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_filename(prefix, extension):
    """Create a unique filename using the current timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension.lstrip('.')}"


def clean_text(text):
    """Clean and normalize text."""
    if text is None:
        return ""

    return " ".join(str(text).strip().split())


def save_text_file(content, filename, directory="generated_documents"):
    """Save text content into a file."""
    output_dir = ensure_output_directory(directory)
    file_path = output_dir / filename

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path


def get_file_size(file_path):
    """Return file size in bytes."""
    path = Path(file_path)

    if path.exists():
        return path.stat().st_size

    return 0