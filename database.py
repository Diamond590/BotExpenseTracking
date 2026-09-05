import sqlite3

def init_db():
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            category TEXT,
            comment TEXT,
            created_at TEXT)""")

    connection.commit()
    connection.close()

def add_expense(user_id, amount, category, comment, created_at):
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO expenses (user_id, amount, category, comment, created_at)
    VALUES (?, ?, ?, ?, ?)""",
        (user_id, amount, category, comment, created_at)
    )

    connection.commit()
    connection.close()

def get_expenses(user_id):
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE user_id = ?
        ORDER BY id DESC""", (user_id,))

    expenses = cursor.fetchall()

    connection.close()

    return expenses