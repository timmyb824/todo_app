import sqlite3

connection = sqlite3.connect('todo.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user VARCHAR(16),
        password VARCHAR(32)
    );"""
)