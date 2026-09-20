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
            category TEXT PRIMARY KEY,
            amount REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            name TEXT PRIMARY KEY,
            target REAL NOT NULL,
            saved REAL NOT NULL DEFAULT 0
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


def save_budget(category, amount):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO budgets (category, amount)
        VALUES (?, ?)
        ON CONFLICT(category)
        DO UPDATE SET amount = excluded.amount
    """, (category, amount))

    connection.commit()
    connection.close()


def load_budgets():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, amount
        FROM budgets
    """)

    rows = cursor.fetchall()
    connection.close()

    return rows


def save_goal(name, target, saved=0):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO goals (name, target, saved)
        VALUES (?, ?, ?)
        ON CONFLICT(name)
        DO UPDATE SET
            target = excluded.target,
            saved = excluded.saved
    """, (name, target, saved))

    connection.commit()
    connection.close()


def load_goals():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, target, saved
        FROM goals
    """)

    rows = cursor.fetchall()
    connection.close()

    return rows