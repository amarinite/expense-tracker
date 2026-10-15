import argparse
import sys
from pathlib import Path

from tracker.logic import add_expense, total
from tracker.models import Expense
from tracker.storage import StorageError, load_book, save_book


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracker",
        description="Track expenses from the command line",
    )

    parser.add_argument(
        "--file",
        type=Path,
        default=Path("data/expenses.json"),
        help="Path to the expense book (default: %(default)s)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add an expense")
    add.add_argument("--amount", type=float, required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--note", default="")

    sub.add_parser("list", help="List all expenses")

    tot = sub.add_parser("total", help="Show the total")
    tot.add_argument("--category", default=None)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        book = load_book(args.file)
    except StorageError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.command == "add":
        try:
            expense = Expense(
                amount=args.amount,
                category=args.category,
                note=args.note,
            )
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1

        add_expense(book, expense)
        save_book(book, args.file)
        print(f"Added: {expense.amount:.2f} [{expense.category}]")
        return 0

    if args.command == "list":
        if not book.expenses:
            print("No expenses yet")
            return 0
        for exp in book.expenses:
            line = f"{exp.amount:8.2f} {exp.category}"
            if exp.note:
                line += f" ({exp.note})"
            print(line)
        return 0

    if args.command == "total":
        result = total(book, category=args.category)
        if args.category is None:
            print(f"Total: {result:.2f}")
        else:
            print(f"Total for '{args.category}': {result:.2f}")
        return 0
    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
