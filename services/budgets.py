from datetime import datetime

from storage import (
    load_budgets,
    load_transactions
)


def get_budget_data(
    year,
    month
):

    budget_rows = load_budgets(
        year,
        month
    )

    transactions = load_transactions()

    result = []

    for row in budget_rows:

        category = row["category"]

        budget = float(
            row["amount"]
        )

        spent = 0

        for transaction in transactions:

            if (
                transaction["transaction_type"]
                != "expense"
            ):
                continue

            if (
                transaction["category"].lower()
                != category.lower()
            ):
                continue

            transaction_date = datetime.strptime(
                transaction["date"],
                "%Y-%m-%d %H:%M"
            )

            if (
                transaction_date.year == year
                and transaction_date.month == month
            ):

                spent += float(
                    transaction["amount"]
                )

        remaining = budget - spent

        percentage = (
            (spent / budget) * 100
            if budget > 0
            else 0
        )

        result.append({
            "category": category,
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
            "percentage": percentage,
            "over_budget": spent > budget
        })

    return result