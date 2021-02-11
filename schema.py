import sqlite3

connection = sqlite3.connect('todo.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(16),
        password VARCHAR(32),
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );"""
)

cursor.execute(
    """CREATE TABLE lists(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );"""
)

cursor.execute(
    """CREATE TABLE items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        list_id INTEGER NOT NULL,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        done INTEGER NOT NULL DEFAULT 0,
        content TEXT NOT NULL,
        due_by DATE NOT NULL,
        FOREIGN KEY (list_id) REFERENCES lists(id)
    );"""
)