from tracker.models import Expense, ExpenseBook


def add_expense(book: ExpenseBook, expense: Expense) -> None:
    book.expenses.append(expense)


def total(book: ExpenseBook, category: str | None = None) -> float:
    return sum(
            e.amount for e in book.expenses
            if category is None or e.category == category
        )
