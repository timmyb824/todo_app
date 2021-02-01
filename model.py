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

#check users by looping through the table
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

#user signup    
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

#read the todos (tasks and items)
def todos(username):
    connection = get_db_connection()
    todos = connection.execute("""SELECT i.id, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id JOIN users u ON l.user_id = u.id WHERE u.username = '{username}' ORDER BY l.title;""".format(username=username)).fetchall()
    lists = {}

    for k, g in groupby(todos, key=lambda t: t['title']):
        lists[k] = list(g)
        
    connection.commit()
    connection.close()
    return lists

#create new todo list or create new task for an existing todo list
def create(username, title, content):
    connection = get_db_connection()
    exist = connection.execute("""SELECT id FROM lists WHERE title ='{title}' AND user_id in (SELECT id FROM users WHERE username='{username}');""".format(username=username,title=title)).fetchone()
  
    if exist is None:
        connection.execute("""INSERT INTO lists(user_id, title)VALUES((SELECT id FROM users WHERE username = '{username}'),'{title}');""".format(username=username, title=title))
        connection.execute("""INSERT INTO items(list_id, content)VALUES((SELECT id FROM lists where title = '{title}'),'{content}');""".format(title=title, content=content))

    else:
        connection.execute("""INSERT INTO items(list_id, content)VALUES((SELECT id FROM lists where title = '{title}'),'{content}');""".format(title=title, content=content))
        connection.commit()
        connection.close()
        return 'New task added to todo'

    connection.commit()
    connection.close()
    return 'New todo created!'

#update todo list name
def edit_title(username, title, new_title):
    connection = get_db_connection()
    connection.execute("""UPDATE lists SET title = '{new_title}' WHERE title = '{title}' and user_id in (SELECT id FROM users WHERE username = '{username}');""".format(username=username,title=title, new_title=new_title))
 
    connection.commit()
    connection.close()
    return 'List name updated!'

#update task name (need to add a username check)
def edit_task(content, new_content):
    connection = get_db_connection()
    connection.execute("""UPDATE items SET content = '{new_content}' WHERE content = '{content}';""".format(new_content=new_content, content=content))
 
    connection.commit()
    connection.close()
    return 'Task name updated!'

#delete todo list (need to add a username check)
def delete(username, title):
    connection = get_db_connection()
    connection.execute("""DELETE FROM items WHERE list_id in (SELECT id FROM lists WHERE title = '{title}');""".format(title=title))
    connection.execute("""DELETE FROM lists WHERE title = '{title}' and user_id in (SELECT id FROM users WHERE username = '{username}');""".format(title=title, username = username))
 
    connection.commit()
    connection.close()
    return 'Todo deleted!'

#delete task (need to add a username check)
def delete_task(content, title):
    connection = get_db_connection()
    connection.execute("""DELETE FROM items WHERE content = '{content}' AND list_id in (SELECT id FROM lists WHERE title = '{title}');""".format(content=content,title=title))
 
    connection.commit()
    connection.close()
    return 'Task deleted!'




