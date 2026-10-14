from pathlib import Path

from tracker.models import Expense
from tracker.storage import StorageError, load_book, save_book

BOOK_PATH =  Path("book.json")


def main() -> None:
    try:
        book = load_book(BOOK_PATH)
    except StorageError as e:
        print(f"Could not load book: {e}")
        raise SystemExit(1)

    book.expenses.append(Expense(amount=12.5, category="food", note="lunch"))
    save_book(book, BOOK_PATH)

    print(book.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
