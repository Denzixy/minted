from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from storage import (
    initialize_database,
    add_transaction,
    load_transactions,
    update_transaction,
    delete_transaction,
)


app = FastAPI(
    title="Minted API",
    description="Personal finance API for the Minted app.",
    version="1.0.0"
)


initialize_database()


# =========================
# REQUEST MODELS
# =========================

class TransactionCreate(BaseModel):
    amount: float = Field(gt=0)
    transaction_type: str
    category: str
    description: str


class TransactionUpdate(BaseModel):
    amount: float = Field(gt=0)
    transaction_type: str
    category: str
    description: str


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "app": "Minted",
        "status": "online"
    }


# =========================
# GET TRANSACTIONS
# =========================

@app.get("/transactions")
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


# =========================
# GET ONE TRANSACTION
# =========================

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):

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
        detail="Transaction not found"
    )


# =========================
# CREATE TRANSACTION
# =========================

@app.post("/transactions")
def create_transaction(
    transaction: TransactionCreate
):

    if transaction.transaction_type not in (
        "income",
        "expense"
    ):
        raise HTTPException(
            status_code=400,
            detail="Transaction type must be income or expense"
        )

    date = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    class DatabaseTransaction:
        pass

    new_transaction = DatabaseTransaction()

    new_transaction.amount = transaction.amount
    new_transaction.transaction_type = (
        transaction.transaction_type
    )
    new_transaction.category = transaction.category
    new_transaction.description = (
        transaction.description
    )
    new_transaction.date = date

    transaction_id = add_transaction(
        new_transaction
    )

    return {
        "message": "Transaction created",
        "id": transaction_id
    }


# =========================
# UPDATE TRANSACTION
# =========================

@app.put("/transactions/{transaction_id}")
def edit_transaction(
    transaction_id: int,
    transaction: TransactionUpdate
):

    if transaction.transaction_type not in (
        "income",
        "expense"
    ):
        raise HTTPException(
            status_code=400,
            detail="Transaction type must be income or expense"
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
            detail="Transaction not found"
        )

    return {
        "message": "Transaction updated",
        "id": transaction_id
    }


# =========================
# DELETE TRANSACTION
# =========================

@app.delete("/transactions/{transaction_id}")
def remove_transaction(transaction_id: int):

    deleted = delete_transaction(
        transaction_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "message": "Transaction deleted",
        "id": transaction_id
    }