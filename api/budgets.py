from fastapi import APIRouter

from pydantic import (
    BaseModel,
    Field
)

from storage import save_budget

from services.budgets import (
    get_budget_data
)


router = APIRouter(
    prefix="/budgets",
    tags=["budgets"]
)


class BudgetCreate(BaseModel):

    category: str

    amount: float = Field(
        gt=0
    )

    year: int

    month: int = Field(
        ge=1,
        le=12
    )


@router.get("")
def get_budgets(
    year: int,
    month: int
):

    return get_budget_data(
        year,
        month
    )


@router.post("")
def create_budget(
    budget: BudgetCreate
):

    save_budget(
        budget.category,
        budget.amount,
        budget.year,
        budget.month
    )

    return {
        "message": "Budget saved successfully."
    }