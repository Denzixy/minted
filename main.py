from datetime import datetime

from models import Transaction

from storage import (
    initialize_database,
    add_transaction as db_add_transaction,
    load_transactions,
    save_budget,
    load_budgets,
    save_goal,
    load_goals,
    update_transaction,
    delete_transaction
)

from analytics import (
    calculate_balance,
    spending_summary,
    monthly_summary,
    show_spending_chart,
    show_monthly_chart
)

from budgets import (
    set_budget,
    get_budget_status
)

from goals import (
    create_goal,
    add_to_goal,
    get_goal_progress
)

from export import export_transactions


transactions = []
budgets = {}
goals = {}

def get_positive_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid number.")


def get_transaction_id(prompt):
    while True:
        try:
            transaction_id = int(input(prompt))

            if transaction_id <= 0:
                print("Enter a valid transaction ID.")
                continue

            return transaction_id

        except ValueError:
            print("Please enter a whole number.")

def show_menu():
    print("\n========== MINTED ==========")
    print("1. Dashboard")
    print("2. Add income")
    print("3. Add expense")
    print("4. View transactions")
    print("5. View balance")
    print("6. Spending summary")
    print("7. Monthly report")
    print("8. Spending chart")
    print("9. Monthly chart")
    print("10. Set budget")
    print("11. View budgets")
    print("12. Create financial goal")
    print("13. Add money to goal")
    print("14. View goals")
    print("15. Edit transaction")
    print("16. Delete transaction")
    print("17. Exit")
    print("18. Export transactions to CSV")


def add_transaction(transaction_type):
    print(f"\n--- Add {transaction_type} ---")

    amount = get_positive_amount("Amount (RM): ")
    category = input("Category: ")
    description = input("Description: ")

    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    transaction = Transaction(
        None,
        amount,
        transaction_type,
        category,
        description,
        date
    )

    transaction_id = db_add_transaction(transaction)

    transaction.transaction_id = transaction_id

    transactions.append(transaction)

    print(f"\nTransaction #{transaction_id} added successfully.")


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

    set_budget(
        budgets,
        category,
        amount
    )

    save_budget(
        category,
        amount
    )

    print(
        f"\nBudget set for {category}: "
        f"RM {amount:.2f}"
    )


def show_budgets():
    status = get_budget_status(
        budgets,
        transactions
    )

    if not status:
        print("\nNo budgets set.")
        return

    print("\n========== BUDGETS ==========")

    for category, data in status.items():

        print(f"\n{category}")

        print(
            f"Spent:     RM {data['spent']:.2f}"
        )

        print(
            f"Budget:    RM {data['budget']:.2f}"
        )

        print(
            f"Remaining: RM {data['remaining']:.2f}"
        )

        print(
            f"Used:      {data['percentage']:.1f}%"
        )


def handle_create_goal():
    name = input("\nGoal name: ")
    target = float(input("Target amount (RM): "))

    create_goal(
        goals,
        name,
        target
    )

    save_goal(
        name,
        target,
        0
    )

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

    amount = float(
        input("Amount to add (RM): ")
    )

    success = add_to_goal(
        goals,
        name,
        amount
    )

    if not success:
        print("\nGoal not found.")
        return

    save_goal(
        name,
        goals[name]["target"],
        goals[name]["saved"]
    )

    print(
        f"\nRM {amount:.2f} added to '{name}'."
    )


def show_goals():
    progress = get_goal_progress(goals)

    if not progress:
        print("\nNo goals available.")
        return

    print("\n========== FINANCIAL GOALS ==========")

    for name, data in progress.items():

        print(f"\n{name}")

        print(
            f"Saved:     RM {data['saved']:.2f}"
        )

        print(
            f"Target:    RM {data['target']:.2f}"
        )

        print(
            f"Remaining: RM {data['remaining']:.2f}"
        )

        print(
            f"Progress:  {data['percentage']:.1f}%"
        )

def edit_transaction():
    if not transactions:
        print("\nNo transactions to edit.")
        return

    show_transactions()

    transaction_id = get_transaction_id(
        "\nEnter transaction ID to edit: "
    )

    transaction = next(
        (
            item for item in transactions
            if item.transaction_id == transaction_id
        ),
        None
    )

    if transaction is None:
        print("\nTransaction not found.")
        return

    print("\nLeave a field blank to keep its current value.")

    print(f"Current amount: RM {transaction.amount:.2f}")
    new_amount = input("New amount: ").strip()

    if new_amount:
        try:
            new_amount = float(new_amount)

            if new_amount <= 0:
                print("Amount must be greater than zero.")
                return

        except ValueError:
            print("Invalid amount.")
            return
    else:
        new_amount = transaction.amount

    print(f"Current type: {transaction.transaction_type}")
    new_type = input("New type (income/expense): ").strip().lower()

    if new_type:
        if new_type not in ("income", "expense"):
            print("Type must be income or expense.")
            return
    else:
        new_type = transaction.transaction_type

    new_category = input(
        f"New category [{transaction.category}]: "
    ).strip()

    if not new_category:
        new_category = transaction.category

    new_description = input(
        f"New description [{transaction.description}]: "
    ).strip()

    if not new_description:
        new_description = transaction.description

    update_transaction(
        transaction_id,
        new_amount,
        new_type,
        new_category,
        new_description
    )

    transaction.amount = new_amount
    transaction.transaction_type = new_type
    transaction.category = new_category
    transaction.description = new_description

    print("\nTransaction updated successfully.")


def remove_transaction():
    if not transactions:
        print("\nNo transactions to delete.")
        return

    show_transactions()

    transaction_id = get_transaction_id(
        "\nEnter transaction ID to delete: "
    )

    transaction = next(
        (
            item for item in transactions
            if item.transaction_id == transaction_id
        ),
        None
    )

    if transaction is None:
        print("\nTransaction not found.")
        return

    print(
        f"\nDelete {transaction.description} "
        f"(RM {transaction.amount:.2f})?"
    )

    confirmation = input("Type YES to confirm: ").strip()

    if confirmation != "YES":
        print("Deletion cancelled.")
        return

    delete_transaction(transaction_id)

    transactions.remove(transaction)

    print("\nTransaction deleted successfully.")

def show_dashboard():
    now = datetime.now()

    year = now.year
    month = now.month

    report = monthly_summary(
        transactions,
        year,
        month
    )

    balance = calculate_balance(transactions)

    print("\n" + "=" * 42)
    print("           MINTED DASHBOARD")
    print("=" * 42)

    print(f"\nMonth: {now.strftime('%B %Y')}")

    print("\n--- OVERALL BALANCE ---")
    print(f"Current balance: RM {balance:.2f}")

    print("\n--- THIS MONTH ---")
    print(f"Income:       RM {report['income']:.2f}")
    print(f"Expenses:     RM {report['expenses']:.2f}")
    print(f"Savings:      RM {report['savings']:.2f}")
    print(f"Savings rate: {report['savings_rate']:.1f}%")

    print("\n--- SPENDING BY CATEGORY ---")

    if report["categories"]:
        for category, amount in sorted(
            report["categories"].items(),
            key=lambda item: item[1],
            reverse=True
        ):
            print(f"{category}: RM {amount:.2f}")
    else:
        print("No expenses recorded this month.")

    print("\n--- BUDGET STATUS ---")

    budget_status = get_budget_status(
        budgets,
        transactions
    )

    if budget_status:
        for category, data in budget_status.items():
            print(
                f"{category}: "
                f"RM {data['spent']:.2f} / "
                f"RM {data['budget']:.2f} "
                f"({data['percentage']:.1f}%)"
            )
    else:
        print("No budgets set.")

    print("\n--- FINANCIAL GOALS ---")

    goal_progress = get_goal_progress(goals)

    if goal_progress:
        for name, data in goal_progress.items():
            print(
                f"{name}: "
                f"RM {data['saved']:.2f} / "
                f"RM {data['target']:.2f} "
                f"({data['percentage']:.1f}%)"
            )
    else:
        print("No financial goals set.")

    print("\n" + "=" * 42)

def load_application_data():

    # Load transactions
    rows = load_transactions()

    for row in rows:

        transaction = Transaction(
            row["id"],
            row["amount"],
            row["transaction_type"],
            row["category"],
            row["description"],
            row["date"]
        )

        transactions.append(transaction)

    # Load budgets
    for row in load_budgets():

        budgets[row["category"]] = row["amount"]

    # Load goals
    for row in load_goals():

        goals[row["name"]] = {
            "target": row["target"],
            "saved": row["saved"]
        }


def main():

    initialize_database()

    load_application_data()

    while True:

        show_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            show_dashboard()

        elif choice == "2":
            add_transaction("income")

        elif choice == "3":
            add_transaction("expense")

        elif choice == "4":
            show_transactions()

        elif choice == "5":
            show_balance()

        elif choice == "6":
            show_spending_summary()

        elif choice == "7":
            show_monthly_report()

        elif choice == "8":
            show_spending_chart(transactions)

        elif choice == "9":
            year = int(input("\nYear: "))
            month = int(input("Month (1-12): "))
            show_monthly_chart(transactions, year, month)

        elif choice == "10":
            handle_set_budget()

        elif choice == "11":
            show_budgets()

        elif choice == "12":
            handle_create_goal()

        elif choice == "13":
            handle_add_to_goal()

        elif choice == "14":
            show_goals()

        elif choice == "15":
            edit_transaction()

        elif choice == "16":
            remove_transaction()

        elif choice == "17":
            print("\nThanks for using Minted.")
            break

        elif choice == "18":
            export_transactions(transactions)

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()