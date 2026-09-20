import json


DATA_FILE = "data.json"


def save_data(transactions, budgets, goals):
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

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return {
            "transactions": [],
            "budgets": {},
            "goals": {}
        }