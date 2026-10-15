from pydantic import BaseModel, field_validator


class Expense(BaseModel):
    amount: float
    category: str
    note: str = ""

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError("amount must be non-negative")
        return v


class ExpenseBook(BaseModel):
    expenses: list[Expense] = []
