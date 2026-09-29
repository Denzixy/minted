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

    with open(
        "data.json",
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    print(
        "Starting migration..."
    )

    transactions = data.get(
        "transactions",
        []
    )

    for transaction_data in transactions:

        transaction = Transaction(
            None,
            transaction_data["amount"],
            transaction_data["transaction_type"],
            transaction_data["category"],
            transaction_data["description"],
            transaction_data["date"]
        )

        transaction_id = add_transaction(
            transaction
        )

        print(
            f"Migrated transaction "
            f"#{transaction_id}: "
            f"{transaction.description}"
        )

    budgets = data.get(
        "budgets",
        {}
    )

    now_year = 2026
    now_month = 9

    for category, amount in budgets.items():

        save_budget(
            category,
            amount,
            now_year,
            now_month
        )

        print(
            f"Migrated budget: "
            f"{category} = "
            f"RM {amount:.2f}"
        )

    goals = data.get(
        "goals",
        {}
    )

    for name, goal in goals.items():

        save_goal(
            name,
            goal["target"],
            goal["saved"],
            None
        )

        print(
            f"Migrated goal: {name}"
        )

    print(
        "\nMigration complete."
    )

    print(
        "Your old JSON data is now in minted.db."
    )


if __name__ == "__main__":
    migrate_data()