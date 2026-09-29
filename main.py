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

from budgets import get_budget_status

from goals import get_goal_progress

from insights import (
    generate_insights,
    compare_with_previous_month
)

from export import export_transactions


transactions = []
budgets = {}
goals = {}


def get_positive_amount(prompt):

    while True:

        try:

            amount = float(
                input(prompt)
            )

            if amount <= 0:

                print(
                    "Amount must be greater than 0."
                )

                continue

            return amount

        except ValueError:

            print(
                "Please enter a valid number."
            )


def get_transaction_id(prompt):

    while True:

        try:

            transaction_id = int(
                input(prompt)
            )

            if transaction_id <= 0:

                print(
                    "ID must be positive."
                )

                continue

            return transaction_id

        except ValueError:

            print(
                "Please enter a valid ID."
            )


def add_transaction(transaction_type):

    amount = get_positive_amount(
        "Amount (RM): "
    )

    category = input(
        "Category: "
    ).strip()

    description = input(
        "Description: "
    ).strip()

    date = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    transaction = Transaction(
        None,
        amount,
        transaction_type,
        category,
        description,
        date
    )

    transaction_id = db_add_transaction(
        transaction
    )

    transaction.transaction_id = transaction_id

    transactions.append(
        transaction
    )

    print(
        f"\nTransaction #{transaction_id} added."
    )


def view_transactions():

    if not transactions:

        print(
            "\nNo transactions found."
        )

        return

    print("\n=== TRANSACTIONS ===")

    for transaction in transactions:

        print(
            f"#{transaction.transaction_id} | "
            f"{transaction.date} | "
            f"{transaction.transaction_type.upper()} | "
            f"{transaction.category} | "
            f"{transaction.description} | "
            f"RM {transaction.amount:.2f}"
        )


def view_balance():

    balance = calculate_balance(
        transactions
    )

    print(
        f"\nCurrent balance: "
        f"RM {balance:.2f}"
    )


def view_spending_summary():

    spending = spending_summary(
        transactions
    )

    if not spending:

        print(
            "\nNo expenses found."
        )

        return

    print(
        "\n=== SPENDING SUMMARY ==="
    )

    for category, amount in sorted(
        spending.items(),
        key=lambda item: item[1],
        reverse=True
    ):

        print(
            f"{category}: "
            f"RM {amount:.2f}"
        )


def monthly_report():

    now = datetime.now()

    report = monthly_summary(
        transactions,
        now.year,
        now.month
    )

    print(
        f"\n=== {now.strftime('%B %Y').upper()} ==="
    )

    print(
        f"Income: "
        f"RM {report['income']:.2f}"
    )

    print(
        f"Expenses: "
        f"RM {report['expenses']:.2f}"
    )

    print(
        f"Savings: "
        f"RM {report['savings']:.2f}"
    )

    print(
        f"Savings rate: "
        f"{report['savings_rate']:.1f}%"
    )


def set_monthly_budget():

    category = input(
        "Category: "
    ).strip()

    amount = get_positive_amount(
        "Budget amount (RM): "
    )

    now = datetime.now()

    save_budget(
        category,
        amount,
        now.year,
        now.month
    )

    budgets[category] = amount

    print(
        "\nBudget saved successfully."
    )


def view_budgets():

    now = datetime.now()

    status = get_budget_status(
        budgets,
        transactions,
        now.year,
        now.month
    )

    if not status:

        print(
            "\nNo budgets found."
        )

        return

    print(
        "\n=== BUDGETS ==="
    )

    for category, data in status.items():

        print(
            f"\n{category}"
        )

        print(
            f"Budget: "
            f"RM {data['budget']:.2f}"
        )

        print(
            f"Spent: "
            f"RM {data['spent']:.2f}"
        )

        print(
            f"Remaining: "
            f"RM {data['remaining']:.2f}"
        )

        print(
            f"Used: "
            f"{data['percentage']:.1f}%"
        )


def create_financial_goal():

    name = input(
        "Goal name: "
    ).strip()

    target = get_positive_amount(
        "Target amount (RM): "
    )

    deadline = input(
        "Deadline (YYYY-MM-DD, optional): "
    ).strip()

    if not deadline:
        deadline = None

    save_goal(
        name,
        target,
        0,
        deadline
    )

    goals[name] = {
        "target": target,
        "saved": 0
    }

    print(
        "\nGoal created successfully."
    )


def add_money_to_goal():

    if not goals:

        print(
            "\nNo goals found."
        )

        return

    name = input(
        "Goal name: "
    ).strip()

    if name not in goals:

        print(
            "Goal not found."
        )

        return

    amount = get_positive_amount(
        "Amount to add (RM): "
    )

    goals[name]["saved"] += amount

    goal = goals[name]

    save_goal(
        name,
        goal["target"],
        goal["saved"]
    )

    print(
        "\nMoney added to goal."
    )


def view_goals():

    progress = get_goal_progress(
        goals
    )

    if not progress:

        print(
            "\nNo goals found."
        )

        return

    print(
        "\n=== FINANCIAL GOALS ==="
    )

    for name, data in progress.items():

        print(
            f"\n{name}"
        )

        print(
            f"Saved: "
            f"RM {data['saved']:.2f} "
            f"/ RM {data['target']:.2f}"
        )

        print(
            f"Remaining: "
            f"RM {data['remaining']:.2f}"
        )

        print(
            f"Progress: "
            f"{data['percentage']:.1f}%"
        )


def edit_transaction():

    transaction_id = get_transaction_id(
        "Transaction ID: "
    )

    transaction = None

    for item in transactions:

        if item.transaction_id == transaction_id:

            transaction = item
            break

    if transaction is None:

        print(
            "\nTransaction not found."
        )

        return

    print(
        "\nLeave a field blank to keep its current value."
    )

    amount_input = input(
        f"Amount [{transaction.amount}]: "
    ).strip()

    category_input = input(
        f"Category [{transaction.category}]: "
    ).strip()

    description_input = input(
        f"Description [{transaction.description}]: "
    ).strip()

    type_input = input(
        f"Type [{transaction.transaction_type}]: "
    ).strip()

    if amount_input:

        try:

            amount = float(
                amount_input
            )

            if amount <= 0:
                raise ValueError

        except ValueError:

            print(
                "Invalid amount."
            )

            return

    else:

        amount = transaction.amount

    category = (
        category_input
        if category_input
        else transaction.category
    )

    description = (
        description_input
        if description_input
        else transaction.description
    )

    transaction_type = (
        type_input
        if type_input
        else transaction.transaction_type
    )

    if transaction_type not in [
        "income",
        "expense"
    ]:

        print(
            "Type must be income or expense."
        )

        return

    updated = update_transaction(
        transaction_id,
        amount,
        transaction_type,
        category,
        description
    )

    if not updated:

        print(
            "Could not update transaction."
        )

        return

    transaction.amount = amount
    transaction.transaction_type = transaction_type
    transaction.category = category
    transaction.description = description

    print(
        "\nTransaction updated."
    )


def remove_transaction():

    transaction_id = get_transaction_id(
        "Transaction ID: "
    )

    deleted = delete_transaction(
        transaction_id
    )

    if not deleted:

        print(
            "\nTransaction not found."
        )

        return

    transactions[:] = [
        transaction
        for transaction in transactions
        if transaction.transaction_id
        != transaction_id
    ]

    print(
        "\nTransaction deleted."
    )


def show_dashboard():

    now = datetime.now()

    report = monthly_summary(
        transactions,
        now.year,
        now.month
    )

    print(
        "\n=============================="
    )

    print(
        "          MINTED"
    )

    print(
        "     PERSONAL FINANCE"
    )

    print(
        "=============================="
    )

    print(
        f"\nBalance: "
        f"RM {calculate_balance(transactions):.2f}"
    )

    print(
        f"Income: "
        f"RM {report['income']:.2f}"
    )

    print(
        f"Expenses: "
        f"RM {report['expenses']:.2f}"
    )

    print(
        f"Savings: "
        f"RM {report['savings']:.2f}"
    )

    print(
        f"Savings rate: "
        f"{report['savings_rate']:.1f}%"
    )

    print("\nInsights:")

    insights = generate_insights(
        transactions,
        now.year,
        now.month
    )

    for insight in insights:

        print(
            f"- {insight}"
        )

    comparison = compare_with_previous_month(
        transactions,
        now.year,
        now.month
    )

    for insight in comparison:

        print(
            f"- {insight}"
        )


def load_application_data():

    transactions.clear()

    rows = load_transactions()

    for row in rows:

        transaction = Transaction(
            row["id"],
            float(row["amount"]),
            row["transaction_type"],
            row["category"],
            row["description"],
            row["date"]
        )

        transactions.append(
            transaction
        )

    budgets.clear()

    now = datetime.now()

    budget_rows = load_budgets(
        now.year,
        now.month
    )

    for row in budget_rows:

        budgets[row["category"]] = float(
            row["amount"]
        )

    goals.clear()

    goal_rows = load_goals()

    for row in goal_rows:

        goals[row["name"]] = {
            "target": float(row["target"]),
            "saved": float(row["saved"])
        }


def main():

    initialize_database()

    load_application_data()

    while True:

        print(
            "\n=============================="
        )

        print(
            "           MINTED"
        )

        print(
            "=============================="
        )

        print(
            "1. Dashboard"
        )

        print(
            "2. Add income"
        )

        print(
            "3. Add expense"
        )

        print(
            "4. View transactions"
        )

        print(
            "5. View balance"
        )

        print(
            "6. Spending summary"
        )

        print(
            "7. Monthly report"
        )

        print(
            "8. Spending chart"
        )

        print(
            "9. Monthly chart"
        )

        print(
            "10. Set budget"
        )

        print(
            "11. View budgets"
        )

        print(
            "12. Create financial goal"
        )

        print(
            "13. Add money to goal"
        )

        print(
            "14. View goals"
        )

        print(
            "15. Edit transaction"
        )

        print(
            "16. Delete transaction"
        )

        print(
            "17. Exit"
        )

        print(
            "18. Export transactions to CSV"
        )

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":

            show_dashboard()

        elif choice == "2":

            add_transaction("income")

        elif choice == "3":

            add_transaction("expense")

        elif choice == "4":

            view_transactions()

        elif choice == "5":

            view_balance()

        elif choice == "6":

            view_spending_summary()

        elif choice == "7":

            monthly_report()

        elif choice == "8":

            show_spending_chart(
                transactions
            )

        elif choice == "9":

            now = datetime.now()

            show_monthly_chart(
                transactions,
                now.year,
                now.month
            )

        elif choice == "10":

            set_monthly_budget()

        elif choice == "11":

            view_budgets()

        elif choice == "12":

            create_financial_goal()

        elif choice == "13":

            add_money_to_goal()

        elif choice == "14":

            view_goals()

        elif choice == "15":

            edit_transaction()

        elif choice == "16":

            remove_transaction()

        elif choice == "17":

            print(
                "\nGoodbye!"
            )

            break

        elif choice == "18":

            export_transactions(
                transactions
            )

        else:

            print(
                "\nInvalid option."
            )


if __name__ == "__main__":
    main()