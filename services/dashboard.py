from datetime import datetime

from storage import (
    load_transactions
)


def get_dashboard_data(
    year,
    month
):

    rows = load_transactions()

    balance = 0
    income = 0
    expenses = 0

    categories = {}

    for row in rows:

        amount = float(
            row["amount"]
        )

        transaction_type = (
            row["transaction_type"]
        )

        if transaction_type == "income":

            balance += amount

        else:

            balance -= amount

        transaction_date = datetime.strptime(
            row["date"],
            "%Y-%m-%d %H:%M"
        )

        if (
            transaction_date.year == year
            and transaction_date.month == month
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
        "year": year,
        "month": month
    }