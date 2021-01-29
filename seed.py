import sqlite3

connection = sqlite3.connect('todo.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    """INSERT INTO users(
        username,
        password
        )VALUES(
            'Timothy',
            'Winter'
        );"""
)


cursor.execute(
    """INSERT INTO lists(
        user_id,
        title
        )VALUES(
            '1',
            'Study'
        );"""
)

cursor.execute(
    """INSERT INTO lists(
        user_id,
        title
        )VALUES(
            '1',
            'Home'
        );"""
)

cursor.execute(
    """INSERT INTO items(
        list_id,
        content
        )VALUES(
            '1',
            'Learn Flask'
        );"""
)

cursor.execute(
    """INSERT INTO items(
        list_id,
        content
        )VALUES(
            '2',
            'Wash Dishes'
        );"""
)

connection.commit()
connection.close()

