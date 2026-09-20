def calculate_balance(transactions):
    balance = 0

    for transaction in transactions:
        if transaction.transaction_type == "income":
            balance += transaction.amount
        else:
            balance -= transaction.amount

    return balance


def spending_summary(transactions):
    spending = {}

    for transaction in transactions:
        if transaction.transaction_type == "expense":

            category = transaction.category

            if category not in spending:
                spending[category] = 0

            spending[category] += transaction.amount

    return spending