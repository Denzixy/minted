import csv
from datetime import datetime


def export_transactions(transactions):
    if not transactions:
        print("\nNo transactions to export.")
        return

    filename = (
        f"minted_transactions_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Date",
            "Type",
            "Category",
            "Description",
            "Amount (RM)"
        ])

        for transaction in transactions:
            writer.writerow([
                transaction.transaction_id,
                transaction.date,
                transaction.transaction_type,
                transaction.category,
                transaction.description,
                f"{transaction.amount:.2f}"
            ])

    print(f"\nTransactions exported successfully!")
    print(f"File: {filename}")