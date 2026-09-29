from datetime import datetime


def set_budget(
    budgets,
    category,
    amount
):
    budgets[category] = amount


def get_budget_status(
    budgets,
    transactions,
    year,
    month
):

    status = {}

    for category, budget in budgets.items():

        spent = 0

        for transaction in transactions:

            if transaction.transaction_type != "expense":
                continue

            if (
                transaction.category.lower()
                != category.lower()
            ):
                continue

            transaction_date = datetime.strptime(
                transaction.date,
                "%Y-%m-%d %H:%M"
            )

            if (
                transaction_date.year == year
                and transaction_date.month == month
            ):
                spent += transaction.amount

        remaining = budget - spent

        percentage = (
            (spent / budget) * 100
            if budget > 0
            else 0
        )

        status[category] = {
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
            "percentage": percentage
        }

    return status