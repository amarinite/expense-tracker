import json
from pathlib import Path

import pytest

from tracker.models import Expense, ExpenseBook
from tracker.storage import StorageError, load_book, save_book


def test_load_missing_file_returns_empty_book(tmp_path: Path):
    book = load_book(tmp_path / "does-not-exist.json")
    assert book.expenses == []


def test_load_invalid_json_raises_storage_error(tmp_path: Path):
    path = tmp_path / "bad.json"
    path.write_text("{ this is not json", encoding="utf-8")

    with pytest.raises(StorageError):
        load_book(path)


def test_load_wrong_shape_raises_storage_error(tmp_path: Path):
    path = tmp_path / "wrong-shape.json"
    path.write_text('{"expenses": "hello"}', encoding="utf-8")

    with pytest.raises(StorageError):
        load_book(path)


def test_save_creates_parent_directories(tmp_path: Path):
    path = tmp_path / "nested" / "dir" / "book.json"
    assert not path.parent.exists()

    save_book(ExpenseBook(), path)

    assert path.exists()


def test_save_then_load_round_trips(tmp_path: Path):
    path = tmp_path / "book.json"
    original = ExpenseBook(expenses=[
        Expense(amount=12.5, category="food", note="lunch"),
        Expense(amount=3.0, category="coffee"),
    ])

    save_book(original, path)
    loaded = load_book(path)

    assert loaded == original


def test_saved_file_is_readable_json(tmp_path: Path):
    path = tmp_path / "book.json"
    save_book(ExpenseBook(expenses=[Expense(amount=1.0, category="food")]), path)

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["expenses"][0]["amount"] == 1.0
