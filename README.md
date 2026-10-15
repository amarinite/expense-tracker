# Expense Tracker

A small command-line expense tracker. Expenses are stored as JSON on disk.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Install

```bash
uv sync
```

## Usage

Add an expense:

```bash
uv run tracker add --amount 12.50 --category food --note lunch
```

List all expenses:

```bash
uv run tracker list
```

Show the total, optionally filtered by category:

```bash
uv run tracker total
uv run tracker total --category food
```

By default the book lives at data/expenses.json. Override it with the
global `--file` flag:

```bash
uv run tracker --file my-book.json add --amount 5 --category coffee
```

## Development

Run the checks (mypy, flake8, pytest):

```bash
uv run check
```

Run the checks and then the program:

```bash
uv run tracker-dev list
```
