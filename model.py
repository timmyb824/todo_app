import sqlite3
from itertools import groupby

#define the database connection
def get_db_connection():
    connection = sqlite3.connect('todo.db', check_same_thread = False)
    connection.row_factory = sqlite3.Row
    return connection

#check password by taking in the username
def check_pw(username):
    connection = get_db_connection()
    password = connection.execute("""SELECT password FROM users WHERE username='{username}' ORDER BY id DESC""".format(username = username)).fetchone()[0]

    connection.commit()
    connection.close()
    return password

def check_users():
    connection = get_db_connection()
    db_users = connection.execute("""SELECT username FROM users ORDER BY id DESC;""").fetchall()
    users = []

    for i in range(len(db_users)):
        person = db_users[i][0]
        users.append(person)

    connection.commit()
    connection.close()
    return users    
    
def signup(username, password):
    connection = get_db_connection()
    exist = connection.execute("""SELECT password FROM users WHERE username='{username}';""".format(username=username)).fetchone()

    if exist is None:
        connection.execute("""INSERT INTO users(username, password)VALUES('{username}', '{password}');""".format(username=username, password=password))
        connection.commit()
        connection.close()
    
    else:
        return ('User already exists!')

    return 'You have successfully signed up!'

#get the todo lists
def todos(username):
    connection = get_db_connection()
    todos = connection.execute("""SELECT i.id, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id JOIN users u ON l.user_id = u.id WHERE u.username = '{username}' ORDER BY l.title;""".format(username=username)).fetchall()
    lists = {}

    for k, g in groupby(todos, key=lambda t: t['title']):
        lists[k] = list(g)
        
    connection.commit()
    connection.close()
    return lists

#add new todo list
def create(username, title, content):
    connection = get_db_connection()
    connection.execute("""INSERT INTO lists(user_id, title)VALUES((SELECT id FROM users WHERE username = '{username}'),'{title}');""".format(username=username, title=title))
    connection.execute("""INSERT INTO items(list_id, content)VALUES((SELECT id FROM lists where title = '{title}'),'{content}');""".format(title=title, content=content))
  
    connection.commit()
    connection.close()
    return 'New todo created!'

#delete todo list
def delete(username, title, content):
    connection = get_db_connection()
    connection.execute("""DELETE FROM items WHERE content = '{content}' and list_id in (SELECT id FROM lists WHERE title = '{title}');""".format(content=content, title=title))
    connection.execute("""DELETE FROM lists WHERE title = '{title}' and user_id in (SELECT id FROM users WHERE username = '{username}');""".format(title=title, username = username))
 
    connection.commit()
    connection.close()
    return 'Todo deleted!'

#edit todo list name
def edit_title(username, title, new_title):
    connection = get_db_connection()
    connection.execute("""UPDATE lists SET title = '{new_title}' WHERE title = '{title}' and user_id in (SELECT id FROM users WHERE username = '{username}');""".format(username=username,title=title, new_title=new_title))
 
    connection.commit()
    connection.close()
    return 'List name updated!'

