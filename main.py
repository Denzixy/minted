import json

class Transaction:
    def __init__(self, amount, transaction_type, category, description):
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.description = description

transactions = []

def show_menu():
    print("\n========== MINTED ==========")
    print("1. Add income")
    print("2. Add expense")
    print("3. View transactions")
    print("4. View balance")
    print("5. Exit")

def add_transaction(transaction_type):
    print(f"\n--- Add {transaction_type} ---")

    amount = float(input("Amount (RM): "))
    category = input("Category: ")
    description = input("Description: ")

    transaction = Transaction(
        amount,
        transaction_type,
        category,
        description
    )

    transactions.append(transaction)

    save_transactions()

    print("Transaction added successfully.")

def show_transactions():
    if not transactions:
        print("\nNo transactions yet.")
        return

    print("\n========== TRANSACTIONS ==========")

    for transaction in transactions:
        print(
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
            print("\nThanks for using Minted.")
            break
        else:
            print("Invalid option.")

def save_transactions():
    data = []

    for transaction in transactions:
        data.append({
            "amount": transaction.amount,
            "transaction_type": transaction.transaction_type,
            "category": transaction.category,
            "description": transaction.description
        })
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def load_transactions():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

            for item in data:
                transaction = Transaction(
                    item["amount"],
                    item["transaction_type"],
                    item["category"],
                    item["description"]
                )

                transactions.append(transaction)
    except FileNotFoundError:
        pass

load_transactions()
main()