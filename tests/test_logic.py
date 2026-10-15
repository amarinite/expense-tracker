import pytest
from pydantic import ValidationError

from tracker.logic import add_expense, total
from tracker.models import Expense, ExpenseBook


def test_empty_book_total_is_zero():
    book = ExpenseBook()
    assert total(book) == 0.0


def test_add_expense_appends():
    book = ExpenseBook()
    add_expense(book, Expense(amount=10.0, category="food"))
    assert len(book.expenses) == 1
    assert total(book) == 10.0


def test_total_filters_by_category():
    book = ExpenseBook(expenses=[
        Expense(amount=10.0, category="food"),
        Expense(amount=5.0, category="travel"),
        Expense(amount=2.5, category="food"),
    ])
    assert total(book) == 17.5
    assert total(book, category="food") == 12.5
    assert total(book, category="travel") == 5.0


def test_negative_amount_is_rejected():
    with pytest.raises(ValidationError):
        Expense(amount=-5.0, category="food")
