import json
from datetime import datetime
next_transaction_id = 1

class Transaction:
    def __init__(
        self,
        transaction_id,
        amount,
        transaction_type,
        category,
        description,
        date
    ):
        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.description = description
        self.date = date

transactions = []
budgets = {}
goals = {}

def show_menu():
    print("\n========== MINTED ==========")
    print("1. Add income")
    print("2. Add expense")
    print("3. View transactions")
    print("4. View balance")
    print("5. Spending summary")
    print("6. Set budget")
    print("7. View budgets")
    print("8. Create financial goals")
    print("9. Add money to goal")
    print("10. View goals")
    print("11. Exit")

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

    save_data()

    print("Transaction added successfully.")

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
    balance = 0

    for transaction in transactions:
        if transaction.transaction_type == "income":
            balance += transaction.amount
        else:
            balance -= transaction.amount

    print(f"\nCurrent balance: RM {balance:.2f}")

def spending_summary():
    if not transactions:
        print("\nNo transactions yet.")
        return

    spending = {}

    for transaction in transactions:
        if transaction.transaction_type == "expense":
            category = transaction.category

            if category not in spending:
                spending[category] = 0

            spending[category] += transaction.amount

    if not spending:
        print("\nNo expenses recorded yet.")
        return

    print("\n========== SPENDING SUMMARY ==========")

    total = 0

    for category, amount in spending.items():
        print(f"{category}: RM {amount:.2f}")
        total += amount

    print("---------------------------------------")
    print(f"Total spending: RM {total:.2f}")

def create_goal():
    name = input("\nGoal name: ")
    target = float(input("Target amount (RM): "))

    goals[name] = {
        "target": target,
        "saved": 0
    }

    save_data()

    print(f"\nGoal '{name}' created.")

def add_to_goal():
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

    goals[name]["saved"] += amount

    save_data()

    print(
        f"\nRM {amount:.2f} added to "
        f"'{name}'."
    )

def show_goals():
    if not goals:
        print("\nNo goals available.")
        return

    print("\n========== FINANCIAL GOALS ==========")

    for name, goal in goals.items():

        target = goal["target"]
        saved = goal["saved"]

        remaining = max(target - saved, 0)

        percentage = (
            (saved / target) * 100
            if target > 0
            else 0
        )

        print(f"\n{name}")
        print(f"Saved:     RM {saved:.2f}")
        print(f"Target:    RM {target:.2f}")
        print(f"Remaining: RM {remaining:.2f}")
        print(f"Progress:  {percentage:.1f}%")

def set_budget():
    category = input("\nCategory: ")
    amount = float(input("Budget amount (RM): "))

    budgets[category] = amount

    save_data()

    print(f"\nBudget set for {category}: RM {amount:.2f}")

def show_budgets():
    if not budgets:
        print("\nNo budgets set.")
        return

    print("\n========== BUDGETS ==========")

    for category, budget in budgets.items():

        spent = 0

        for transaction in transactions:
            if (
                transaction.transaction_type == "expense"
                and transaction.category.lower() == category.lower()
            ):
                spent += transaction.amount

        remaining = budget - spent

        percentage = (spent / budget) * 100 if budget > 0 else 0

        print(f"\n{category}")
        print(f"Spent:     RM {spent:.2f}")
        print(f"Budget:    RM {budget:.2f}")
        print(f"Remaning:  RM {remaining:.2f}")
        print(f"Used:      {percentage:.1f}%")

def main():
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
            spending_summary()
        elif choice == "6":
            set_budget()
        elif choice == "7":
            show_budgets()
        elif choice == "8":
            create_goal()
        elif choice == "9":
            add_to_goal()
        elif choice == "10":
            show_goals()
        elif choice == "11":
            print("\nThanks for using Minted.")
            break
        else:
            print("\nInvalid option.")

def save_data():
    data = {
        "transactions": [],
        "budgets": budgets,
        "goals": goals
    }

    for transaction in transactions:
        data["transactions"].append({
            "transaction_id": transaction.transaction_id,
            "amount": transaction.amount,
            "transaction_type": transaction.transaction_type,
            "category": transaction.category,
            "description": transaction.description,
            "date": transaction.date
        })

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    global next_transaction_id

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

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

    except FileNotFoundError:
        pass

load_data()
main()