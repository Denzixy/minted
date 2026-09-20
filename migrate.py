import json

from models import Transaction
from storage import (
    initialize_database,
    add_transaction,
    save_budget,
    save_goal
)


def migrate_data():
    initialize_database()

    with open("data.json", "r") as file:
        data = json.load(file)

    print("Starting migration...")

    # -------------------------
    # TRANSACTIONS
    # -------------------------

    transactions = data.get("transactions", [])

    for transaction_data in transactions:

        transaction = Transaction(
            None,
            transaction_data["amount"],
            transaction_data["transaction_type"],
            transaction_data["category"],
            transaction_data["description"],
            transaction_data["date"]
        )

        transaction_id = add_transaction(transaction)

        print(
            f"Migrated transaction #{transaction_id}: "
            f"{transaction.description}"
        )

    # -------------------------
    # BUDGETS
    # -------------------------

    budgets = data.get("budgets", {})

    for category, amount in budgets.items():

        save_budget(
            category,
            amount
        )

        print(
            f"Migrated budget: "
            f"{category} = RM {amount:.2f}"
        )

    # -------------------------
    # GOALS
    # -------------------------

    goals = data.get("goals", {})

    for name, goal in goals.items():

        save_goal(
            name,
            goal["target"],
            goal["saved"]
        )

        print(
            f"Migrated goal: "
            f"{name}"
        )

    print("\nMigration complete.")
    print("Your old JSON data is now in minted.db.")


if __name__ == "__main__":
    migrate_data()