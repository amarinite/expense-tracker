import json
from pathlib import Path
from pydantic import ValidationError
from tracker.models import ExpenseBook


class StorageError(Exception):
    """Raised when the on-disk book can't be read or parsed"""


def load_book(path: Path) -> ExpenseBook:
    """Load an expense book from a JSON file

    Args:
        path: Location of the JSON file

    Returns:
        The loaded book, or an empty one if the file doesn't exist

    Raises:
        StorageError: If the file can't be parsed or has the wrong shape
    """
    if not path.exists():
        return ExpenseBook()

    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise StorageError(f"invalid JSON: {e}") from e

    try:
        return ExpenseBook.model_validate(data)
    except ValidationError as e:
        raise StorageError(f"invalid file structure: {e}") from e


def save_book(book: ExpenseBook, path: Path) -> None:
    """Saves an expense book to a JSON file

    Args:
        ExpenseBook: the ExpenseBook to save
        path: Location of the JSON file
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(book.model_dump_json(indent=2))
