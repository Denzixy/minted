def set_budget(budgets, category, amount):
    budgets[category] = amount


def get_budget_status(budgets, transactions):

    status = {}

    for category, budget in budgets.items():

        spent = 0

        for transaction in transactions:
            if (
                transaction.transaction_type == "expense"
                and transaction.category.lower() == category.lower()
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