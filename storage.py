import sqlite3

DATABASE = "minted.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,

            PRIMARY KEY (
                category,
                year,
                month
            )
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            name TEXT PRIMARY KEY,
            target REAL NOT NULL,
            saved REAL NOT NULL DEFAULT 0,
            deadline TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_transaction(transaction):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions (
            amount,
            transaction_type,
            category,
            description,
            date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction.amount,
        transaction.transaction_type,
        transaction.category,
        transaction.description,
        transaction.date
    ))

    connection.commit()

    transaction_id = cursor.lastrowid

    connection.close()

    return transaction_id


def load_transactions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def update_transaction(
    transaction_id,
    amount,
    transaction_type,
    category,
    description
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions
        SET amount = ?,
            transaction_type = ?,
            category = ?,
            description = ?
        WHERE id = ?
    """, (
        amount,
        transaction_type,
        category,
        description,
        transaction_id
    ))

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


def delete_transaction(transaction_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM transactions
        WHERE id = ?
    """, (transaction_id,))

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


def save_budget(category, amount, year, month):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO budgets (
            category,
            amount,
            year,
            month
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(category, year, month)
        DO UPDATE SET
            amount = excluded.amount
    """, (
        category,
        amount,
        year,
        month
    ))

    connection.commit()
    connection.close()


def load_budgets(year, month):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            amount,
            year,
            month
        FROM budgets
        WHERE year = ?
        AND month = ?
        ORDER BY category
    """, (
        year,
        month
    ))

    rows = cursor.fetchall()

    connection.close()

    return rows


def save_goal(
    name,
    target,
    saved=0,
    deadline=None
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO goals (
            name,
            target,
            saved,
            deadline
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(name)
        DO UPDATE SET
            target = excluded.target,
            saved = excluded.saved,
            deadline = excluded.deadline
    """, (
        name,
        target,
        saved,
        deadline
    ))

    connection.commit()
    connection.close()


def load_goals():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            name,
            target,
            saved,
            deadline
        FROM goals
        ORDER BY name
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows