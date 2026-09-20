from datetime import datetime

from models import Transaction
from storage import save_data, load_data
from analytics import (
    calculate_balance,
    spending_summary,
    monthly_summary,
    show_spending_chart,
    show_monthly_chart
)
from budgets import set_budget, get_budget_status
from goals import create_goal, add_to_goal, get_goal_progress


transactions = []
budgets = {}
goals = {}

next_transaction_id = 1


def show_menu():
    print("\n========== MINTED ==========")
    print("1. Add income")
    print("2. Add expense")
    print("3. View transactions")
    print("4. View balance")
    print("5. Spending summary")
    print("6. Monthly report")
    print("7. Spending chart")
    print("8. Monthly chart")
    print("9. Set budget")
    print("10. View budgets")
    print("11. Create financial goal")
    print("12. Add money to goal")
    print("13. View goals")
    print("14. Exit")


def add_transaction(transaction_type):

    global next_transaction_id

    print(f"\n--- Add {transaction_type} ---")

    amount = float(input("Amount (RM): "))
    category = input("Category: ")
    description = input("Description: ")

    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    transaction = Transaction(
        next_transaction_id,
        amount,
        transaction_type,
        category,
        description,
        date
    )

    transactions.append(transaction)

    next_transaction_id += 1

    save_data(transactions, budgets, goals)

    print("\nTransaction added successfully.")


def show_transactions():

    if not transactions:
        print("\nNo transactions yet.")
        return

    print("\n========== TRANSACTIONS ==========")

    for transaction in transactions:

        print(
            f"#{transaction.transaction_id} | "
            f"{transaction.date} | "
            f"RM {transaction.amount:.2f} | "
            f"{transaction.transaction_type.upper()} | "
            f"{transaction.category} | "
            f"{transaction.description}"
        )


def show_balance():

    balance = calculate_balance(transactions)

    print(f"\nCurrent balance: RM {balance:.2f}")


def show_spending_summary():

    spending = spending_summary(transactions)

    if not spending:
        print("\nNo expenses recorded yet.")
        return

    print("\n========== SPENDING SUMMARY ==========")

    total = 0

    for category, amount in spending.items():

        print(f"{category}: RM {amount:.2f}")

        total += amount

    print("--------------------------------------")
    print(f"Total spending: RM {total:.2f}")

def show_monthly_report():

    year = int(input("\nYear: "))
    month = int(input("Month (1-12): "))

    report = monthly_summary(
        transactions,
        year,
        month
    )

    print("\n========== MONTHLY REPORT ==========")

    print(f"Income:       RM {report['income']:.2f}")
    print(f"Expenses:     RM {report['expenses']:.2f}")
    print(f"Savings:      RM {report['savings']:.2f}")
    print(f"Savings rate: {report['savings_rate']:.1f}%")

    if report["categories"]:

        print("\nSpending by category:")

        for category, amount in report["categories"].items():
            print(f"{category}: RM {amount:.2f}")

    else:

        print("\nNo expenses recorded this month.")

def handle_set_budget():

    category = input("\nCategory: ")
    amount = float(input("Budget amount (RM): "))

    set_budget(budgets, category, amount)

    save_data(transactions, budgets, goals)

    print(f"\nBudget set for {category}: RM {amount:.2f}")


def show_budgets():

    status = get_budget_status(budgets, transactions)

    if not status:
        print("\nNo budgets set.")
        return

    print("\n========== BUDGETS ==========")

    for category, data in status.items():

        print(f"\n{category}")
        print(f"Spent:     RM {data['spent']:.2f}")
        print(f"Budget:    RM {data['budget']:.2f}")
        print(f"Remaining: RM {data['remaining']:.2f}")
        print(f"Used:      {data['percentage']:.1f}%")


def handle_create_goal():

    name = input("\nGoal name: ")
    target = float(input("Target amount (RM): "))

    create_goal(goals, name, target)

    save_data(transactions, budgets, goals)

    print(f"\nGoal '{name}' created.")


def handle_add_to_goal():

    if not goals:
        print("\nNo goals available.")
        return

    print("\n========== GOALS ==========")

    for name in goals:
        print(f"- {name}")

    name = input("\nWhich goal? ")

    if name not in goals:
        print("\nGoal not found.")
        return

    amount = float(input("Amount to add (RM): "))

    add_to_goal(goals, name, amount)

    save_data(transactions, budgets, goals)

    print(f"\nRM {amount:.2f} added to '{name}'.")


def show_goals():

    progress = get_goal_progress(goals)

    if not progress:
        print("\nNo goals available.")
        return

    print("\n========== FINANCIAL GOALS ==========")

    for name, data in progress.items():

        print(f"\n{name}")
        print(f"Saved:     RM {data['saved']:.2f}")
        print(f"Target:    RM {data['target']:.2f}")
        print(f"Remaining: RM {data['remaining']:.2f}")
        print(f"Progress:  {data['percentage']:.1f}%")


def load_application_data():

    global next_transaction_id

    data = load_data()

    for item in data["transactions"]:

        transaction = Transaction(
            item["transaction_id"],
            item["amount"],
            item["transaction_type"],
            item["category"],
            item["description"],
            item["date"]
        )

        transactions.append(transaction)

    budgets.update(data.get("budgets", {}))
    goals.update(data.get("goals", {}))

    if transactions:

        next_transaction_id = max(
            transaction.transaction_id
            for transaction in transactions
        ) + 1


def main():

    load_application_data()

    while True:

        show_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_transaction("income")

        elif choice == "2":
            add_transaction("expense")

        elif choice == "3":
            show_transactions()

        elif choice == "4":
            show_balance()

        elif choice == "5":
            show_spending_summary()

        elif choice == "6":
            show_monthly_report()

        elif choice == "7":
            show_spending_chart(transactions)

        elif choice == "8":
            year = int(input("\nYear: "))
            month = int(input("Month (1-12): "))

            show_monthly_chart(
            transactions,
            year,
            month
            )

        elif choice == "9":
            handle_set_budget()

        elif choice == "10":
            show_budgets()

        elif choice == "11":
            handle_create_goal()

        elif choice == "12":
            handle_add_to_goal()

        elif choice == "13":
            show_goals()

        elif choice == "14":
            print("\nThanks for using Minted.")
            break

        else:
            print("\nInvalid option.")


main()