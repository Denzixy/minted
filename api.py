from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles

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

@app.get("/dashboard")
def get_dashboard():
    rows = load_transactions()

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    balance = 0
    income = 0
    expenses = 0
    categories = {}

    for row in rows:
        amount = float(row["amount"])
        transaction_type = row["transaction_type"]

        # All-time balance
        if transaction_type == "income":
            balance += amount
        else:
            balance -= amount

        # Current-month analytics
        transaction_date = datetime.strptime(
            row["date"],
            "%Y-%m-%d %H:%M"
        )

        if (
            transaction_date.year == current_year
            and transaction_date.month == current_month
        ):
            if transaction_type == "income":
                income += amount

            elif transaction_type == "expense":
                expenses += amount

                category = row["category"]

                if category not in categories:
                    categories[category] = 0

                categories[category] += amount

    savings = income - expenses

    savings_rate = (
        (savings / income) * 100
        if income > 0
        else 0
    )

    top_category = None

    if categories:
        top_category = max(
            categories,
            key=categories.get
        )

    return {
        "balance": balance,
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate,
        "top_category": top_category,
        "spending": categories,
        "month": f"{current_year}-{current_month:02d}"
    }

app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)