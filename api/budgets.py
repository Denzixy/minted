from fastapi import APIRouter, HTTPException

from pydantic import (
    BaseModel,
    Field
)

from storage import save_budget, delete_budget

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

@router.put("/{category}")
def update_budget(category: str, budget: BudgetCreate):
    save_budget(
        category,
        budget.amount,
        budget.year,
        budget.month
    )

    return {"message": "Budget updated successfully."}


@router.delete("/{category}")
def remove_budget(
    category: str,
    year: int,
    month: int
):
    deleted = delete_budget(category, year, month)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Budget not found."
        )

    return {"message": "Budget deleted successfully."}