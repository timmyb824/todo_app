import sqlite3
import datetime
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
def signup(username, hashed_pass):
    connection = get_db_connection()
    exist = connection.execute("""SELECT password FROM users WHERE username='{username}';""".format(username=username)).fetchone()

    if exist is None:
        connection.execute("""INSERT INTO users(username, password)VALUES('{username}', '{hashed_pass}');""".format(username=username, hashed_pass=hashed_pass))
        connection.commit()
        connection.close()
    
    else:
        return ('User already exists!')

    return 'You have successfully signed up! Please return to the homepage and login!'

#read the todos (tasks and items)
def todos(username):
    connection = get_db_connection()
    todos = connection.execute("""SELECT i.id, i.done, i.content, i.due_by, l.title FROM items i JOIN lists l ON i.list_id = l.id JOIN users u ON l.user_id = u.id WHERE u.username = '{username}' ORDER BY l.title;""".format(username=username)).fetchall()
    lists = {}

    for k, g in groupby(todos, key=lambda t: t['title']):
        lists[k] = list(g)
        
    connection.commit()
    connection.close()
    return lists


#create new todo list or create new task for an existing todo list
def create(username, title, content, due_by):
    connection = get_db_connection()
    exist = connection.execute("""SELECT id FROM lists WHERE title ='{title}' AND user_id in (SELECT id FROM users WHERE username='{username}');""".format(username=username,title=title)).fetchone()
  
    if exist is None:
        connection.execute("""INSERT INTO lists(user_id, title)VALUES((SELECT id FROM users WHERE username = '{username}'),'{title}');""".format(username=username, title=title))
        connection.execute("""INSERT INTO items(list_id, content, due_by)VALUES((SELECT id FROM lists where title = '{title}'),'{content}','{due_by}');""".format(title=title, content=content, due_by=due_by))

    else:
        connection.execute("""INSERT INTO items(list_id, content, due_by)VALUES((SELECT id FROM lists where title = '{title}'),'{content}','{due_by}');""".format(title=title, content=content,due_by=due_by))
        connection.commit()
        connection.close()
        return 'New task added to existing list with that name'

    connection.commit()
    connection.close()
    return 'New todo created!'


#create new task for an existing todo list
def add_task(title, content, due_by):
    connection = get_db_connection()
    connection.execute("""INSERT INTO items(list_id, content, due_by)VALUES((SELECT id FROM lists WHERE title = '{title}'),'{content}','{due_by}');""".format(title=title, content=content,due_by=due_by))
    
    connection.commit()
    connection.close()
    return 'New task added!'

#update todo list name
def edit_title(username, title, new_title):
    connection = get_db_connection()
    connection.execute("""UPDATE lists SET title = '{new_title}' WHERE title = '{title}' and user_id in (SELECT id FROM users WHERE username = '{username}');""".format(username=username,title=title, new_title=new_title))
 
    connection.commit()
    connection.close()
    return 'List name updated!'

#update due by (need to add a username check)
def edit_task(content, new_content):
    connection = get_db_connection()
    connection.execute("""UPDATE items SET content = '{new_content}' WHERE content = '{content}';""".format(new_content=new_content, content=content))
 
    connection.commit()
    connection.close()
    return 'Task name updated!'    

#update task name (need to add a username check)
def edit_dueby(content, due_by):
    connection = get_db_connection()
    connection.execute("""UPDATE items SET due_by = '{due_by}' WHERE content = '{content}';""".format(content=content, due_by=due_by))
 
    connection.commit()
    connection.close()
    return 'Due by updated!'

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

#define "done" action
def done(id):
    connection = get_db_connection()
    connection.execute("""UPDATE items SET done = 1 WHERE id = {id}""".format(id = id))

    connection.commit()
    connection.close()
    

#define "undone" action
def undone(id):
    connection = get_db_connection()
    connection.execute("""UPDATE items SET done = 0 WHERE id = {id}""".format(id = id))

    connection.commit()
    connection.close()

#how many lists the user currently has
def listcount(username):
    connection = get_db_connection()
    listcount = connection.execute("""SELECT COUNT(DISTINCT id) FROM lists WHERE user_id in (SELECT id FROM users WHERE username = '{username}');""".format(username=username)).fetchone()[0]

    connection.commit()
    connection.close()
    return listcount

#how many tasks the user currently has
def taskcount(username):
    connection = get_db_connection()
    taskcount = connection.execute("""SELECT COUNT(DISTINCT id) FROM items WHERE list_id in (SELECT id FROM lists WHERE user_id in (SELECT id FROM users WHERE username = '{username}'));""".format(username=username)).fetchone()[0]
    
    connection.commit()
    connection.close()
    return taskcount

#how many tasks are done
def donecount(username):
    connection = get_db_connection()
    donecount = connection.execute("""SELECT COUNT(DISTINCT id) FROM items WHERE done = 1 AND list_id in (SELECT id FROM lists WHERE user_id in (SELECT id FROM users WHERE username = '{username}'));""".format(username=username)).fetchone()[0]
    
    connection.commit()
    connection.close()
    return donecount

def undonecount(username):
    connection = get_db_connection()
    undonecount = connection.execute("""SELECT COUNT(DISTINCT id) FROM items WHERE done = 0 AND list_id in (SELECT id FROM lists WHERE user_id in (SELECT id FROM users WHERE username = '{username}'));""".format(username=username)).fetchone()[0]
    
    connection.commit()
    connection.close()
    return undonecount

#read the todos due today
def todos_today(username):
    connection = get_db_connection()
    todostoday = connection.execute("""SELECT i.id, i.done, i.content, i.due_by, l.title FROM items i JOIN lists l ON i.list_id = l.id JOIN users u ON l.user_id = u.id WHERE u.username = '{username}' and due_by = date('now') ORDER BY l.title;""".format(username=username)).fetchall()
    liststoday = {}

    for k, g in groupby(todostoday, key=lambda t: t['title']):
        liststoday[k] = list(g)
        
    connection.commit()
    connection.close()
    return liststoday

#read the todos due in the next 7 days
def todos_week(username):
    connection = get_db_connection()
    todosweek = connection.execute("""SELECT i.id, i.done, i.content, i.due_by, l.title FROM items i JOIN lists l ON i.list_id = l.id JOIN users u ON l.user_id = u.id WHERE u.username = '{username}' and due_by between date('now', '1 days') and date('now', '6 days') ORDER BY l.title;""".format(username=username)).fetchall()
    listsweek = {}

    for k, g in groupby(todosweek, key=lambda t: t['title']):
        listsweek[k] = list(g)
        
    connection.commit()
    connection.close()
    return listsweek

#read the todos due in the month plus
def todos_month(username):
    connection = get_db_connection()
    todosmonth = connection.execute("""SELECT i.id, i.done, i.content, i.due_by, l.title FROM items i JOIN lists l ON i.list_id = l.id JOIN users u ON l.user_id = u.id WHERE u.username = '{username}' and due_by > date('now', '6 days') ORDER BY l.title;""".format(username=username)).fetchall()
    listsmonth = {}

    for k, g in groupby(todosmonth, key=lambda t: t['title']):
        listsmonth[k] = list(g)
        
    connection.commit()
    connection.close()
    return listsmonth


 ##########ADMIN PAGE CODE BELOW##########   

#check admin password by taking in the username
def check_admin_pw(user):
    connection = get_db_connection()
    password = connection.execute("""SELECT password FROM admins WHERE user='{user}' ORDER BY id DESC""".format(user = user)).fetchone()[0]

    connection.commit()
    connection.close()
    return password


#check users by looping through the table
def check_admins():
    connection = get_db_connection()
    db_admins = connection.execute("""SELECT user FROM admins ORDER BY id DESC;""").fetchall()
    admins = []

    for i in range(len(db_admins)):
        person = db_admins[i][0]
        admins.append(person)

    connection.commit()
    connection.close()
    return admins   

#total user signups
def signups():
    connection = get_db_connection()
    signups = connection.execute("""SELECT COUNT(DISTINCT id) FROM users;""").fetchone()[0]
    
    connection.commit()
    connection.close()
    return signups

#total user signups in the last 24hrs
def signups24():
    connection = get_db_connection()
    signups24 = connection.execute("""SELECT COUNT(DISTINCT id) FROM users WHERE created >= date('now', '-1 days');""").fetchone()[0]
    
    connection.commit()
    connection.close()
    return signups24

#total lists created
def lists():
    connection = get_db_connection()
    signups = connection.execute("""SELECT COUNT(DISTINCT id) FROM lists;""").fetchone()[0]
    
    connection.commit()
    connection.close()
    return signups

#total lists created in the last 24hrs
def lists24():
    connection = get_db_connection()
    signups24 = connection.execute("""SELECT COUNT(DISTINCT id) FROM lists WHERE created >= date('now', '-1 days');""").fetchone()[0]
    
    connection.commit()
    connection.close()
    return signups24

#get all users 
def all_users():
    connection = get_db_connection()
    users = connection.execute("""SELECT username FROM users ORDER BY id;""").fetchall()

    connection.commit()
    connection.close()
    return users

#get a user
def a_user(username):
    connection = get_db_connection()
    user = connection.execute("""SELECT * FROM users WHERE username = '{username}';""".format(username = username)).fetchone()

    connection.commit()
    connection.close()
    return user


#delete user and lists (need to add a username check)
def delete_user(username):
    connection = get_db_connection()
    connection.execute("""DELETE FROM items WHERE list_id in (SELECT id FROM lists WHERE user_id in (SELECT id FROM users WHERE username = '{username}'));""".format(username=username))
    connection.execute("""DELETE FROM lists WHERE user_id in (SELECT id FROM users WHERE username = '{username}');""".format(username = username))
    connection.execute("""DELETE FROM users WHERE username = '{username}';""".format(username=username))
 
    connection.commit()
    connection.close()
    return 'User and any lists they created have been deleted'




