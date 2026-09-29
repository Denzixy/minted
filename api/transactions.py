from datetime import datetime

from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import BaseModel, Field

from storage import (
    add_transaction,
    load_transactions,
    update_transaction,
    delete_transaction
)


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)


class TransactionCreate(BaseModel):

    amount: float = Field(
        gt=0
    )

    transaction_type: str

    category: str

    description: str


class TransactionUpdate(BaseModel):

    amount: float = Field(
        gt=0
    )

    transaction_type: str

    category: str

    description: str


@router.get("")
def get_transactions():

    rows = load_transactions()

    return [
        {
            "id": row["id"],
            "amount": row["amount"],
            "type": row["transaction_type"],
            "category": row["category"],
            "description": row["description"],
            "date": row["date"]
        }

        for row in rows
    ]


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int
):

    rows = load_transactions()

    for row in rows:

        if row["id"] == transaction_id:

            return {
                "id": row["id"],
                "amount": row["amount"],
                "type": row["transaction_type"],
                "category": row["category"],
                "description": row["description"],
                "date": row["date"]
            }

    raise HTTPException(
        status_code=404,
        detail="Transaction not found."
    )


@router.post("")
def create_transaction(
    transaction: TransactionCreate
):

    if transaction.transaction_type not in [
        "income",
        "expense"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Type must be income or expense."
        )

    class NewTransaction:
        pass

    new_transaction = NewTransaction()

    new_transaction.amount = (
        transaction.amount
    )

    new_transaction.transaction_type = (
        transaction.transaction_type
    )

    new_transaction.category = (
        transaction.category
    )

    new_transaction.description = (
        transaction.description
    )

    new_transaction.date = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
    )

    transaction_id = add_transaction(
        new_transaction
    )

    return {
        "message": "Transaction created.",
        "id": transaction_id
    }


@router.put("/{transaction_id}")
def edit_transaction(
    transaction_id: int,
    transaction: TransactionUpdate
):

    if transaction.transaction_type not in [
        "income",
        "expense"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Type must be income or expense."
        )

    updated = update_transaction(
        transaction_id,
        transaction.amount,
        transaction.transaction_type,
        transaction.category,
        transaction.description
    )

    if not updated:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found."
        )

    return {
        "message": "Transaction updated."
    }


@router.delete("/{transaction_id}")
def remove_transaction(
    transaction_id: int
):

    deleted = delete_transaction(
        transaction_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found."
        )

    return {
        "message": "Transaction deleted."
    }