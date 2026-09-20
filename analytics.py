from datetime import datetime
import matplotlib.pyplot as plt


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


def monthly_summary(transactions, year, month):
    income = 0
    expenses = 0
    categories = {}

    for transaction in transactions:

        transaction_date = datetime.strptime(
            transaction.date,
            "%Y-%m-%d %H:%M"
        )

        if (
            transaction_date.year == year
            and transaction_date.month == month
        ):

            if transaction.transaction_type == "income":

                income += transaction.amount

            else:

                expenses += transaction.amount

                category = transaction.category

                if category not in categories:
                    categories[category] = 0

                categories[category] += transaction.amount

    savings = income - expenses

    savings_rate = (
        (savings / income) * 100
        if income > 0
        else 0
    )

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate,
        "categories": categories
    }

def show_spending_chart(transactions):
    spending = spending_summary(transactions)

    if not spending:
        print("\nNo expenses available for chart.")
        return

    categories = list(spending.keys())
    amounts = list(spending.values())

    plt.figure(figsize=(10, 6))

    plt.bar(categories, amounts)

    plt.title("Minted - Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (RM)")

    plt.tight_layout()
    plt.show()

def show_monthly_chart(transactions, year, month):
    report = monthly_summary(
        transactions,
        year,
        month
    )

    categories = ["Income", "Expenses", "Savings"]

    values = [
        report["income"],
        report["expenses"],
        report["savings"]
    ]

    plt.figure(figsize=(8, 6))

    plt.bar(categories, values)

    plt.title(
        f"Minted - {year}-{month:02d}"
    )

    plt.ylabel("Amount (RM)")

    plt.tight_layout()
    plt.show()