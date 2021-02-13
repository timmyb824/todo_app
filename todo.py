#import the model file making sure the name is unique
#g is global variable for flask
from flask import Flask, render_template, request, session, redirect, url_for, g, flash
from passlib.hash import pbkdf2_sha256
from datetime import date
import model

#set secret key from config file
app = Flask(__name__)
app.config.from_pyfile('config.py')

#check users in the database
username = ''
user = model.check_users()

#if users is already logged in then dashbboard otherwise homepage
@app.route('/', methods = ['GET'])
def home():
    if 'username' in session:
        g.user=session['username']
        lists = model.todos(g.user)
        listcount = model.listcount(g.user)
        taskcount = model.taskcount(g.user)
        donecount = model.donecount(g.user)
        undonecount = model.undonecount(g.user)
        return render_template('public/dashboard.html', lists = lists, listcount = listcount, taskcount = taskcount, donecount = donecount, undonecount = undonecount)
    return render_template('public/homepage.html', message = 'Login or sign up')

#If user exists and and password is valid then login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None)
        areyouuser = request.form['username']
        pwd = model.check_pw(areyouuser)
        if areyouuser is not None and pbkdf2_sha256.verify(request.form['password'], pwd):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('public/homepage.html', message = 'There is a problem logging you in')

#load user from session to run befor each request
@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

#define user signup and store password as a hash
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        message = 'Please sign up!'
        return render_template('public/signup.html', message = message)
    else:
        username = request.form['username']
        password = request.form['password']
        hashed_pass = pbkdf2_sha256.hash(str(password))
        message = model.signup(username, hashed_pass)
        return render_template('public/signup.html', message = message)

@app.route('/getsession')
def getsession():
    if 'username' in session:
        return session['username']
    return redirect(url_for('login'))

#log user out and return home
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('home'))

#render the create new list or task page
@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        content = request.form['content']
        due_by = request.form['due_by']
        message = model.create(username, title, content, due_by)
        return render_template('public/create.html', message = message )
    else:
        return render_template('public/create.html')

#render the create new task page
@app.route('/add-task', methods = ['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        content = request.form['content']
        due_by = request.form['due_by']
        lists = model.todos(username)
        message = model.add_task(title, content, due_by)
        return render_template('public/add_task.html', lists = lists, message = message )
    else:
        username = session['username']
        lists = model.todos(username)
        return render_template('public/add_task.html', lists = lists)

#render the edit list name page
@app.route('/edit-title', methods = ['GET', 'POST'])
def edit_title():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        new_title = request.form['new_title']
        lists = model.todos(username)
        message = model.edit_title(username, title, new_title)
        return render_template('public/edit_title.html', message = message, lists = lists )
    else:
        username = session['username']
        lists = model.todos(username)
        return render_template('public/edit_title.html', lists = lists)

#render the edit task page
@app.route('/edit-task', methods = ['GET', 'POST'])
def edit_task():
    if request.method == 'POST':
        content = request.form['content']
        new_content = request.form['new_content']
        username = session['username']
        lists = model.todos(username)
        message = model.edit_task(content, new_content)
        return render_template('public/edit_task.html', message = message, lists = lists )
    else:
        username = session['username']
        lists = model.todos(username)
        return render_template('public/edit_task.html', lists = lists)

#render the edit due by page
@app.route('/edit-dueby', methods = ['GET', 'POST'])
def edit_dueby():
    if request.method == 'POST':
        content = request.form['content']
        due_by = request.form['due_by']
        username = session['username']
        lists = model.todos(username)
        message = model.edit_dueby(content, due_by)
        return render_template('public/edit_dueby.html', message = message, lists = lists )
    else:
        username = session['username']
        lists = model.todos(username)
        return render_template('public/edit_dueby.html', lists = lists)

#render the delete list page
@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        lists = model.todos(username)
        message = model.delete(username, title)
        return render_template('public/delete.html', message = message, lists = lists )
    else:
        username = session['username']
        lists = model.todos(username)
        return render_template('public/delete.html', lists = lists)

#render the delete task page
@app.route('/delete-task', methods = ['GET', 'POST'])
def delete_task():
    if request.method == 'POST':
        content = request.form['content']
        title = request.form['title']
        username = session['username']
        lists = model.todos(username)
        message = model.delete_task(content, title)
        return render_template('public/delete_task.html', message = message, lists = lists )
    else:
        username = session['username']
        lists = model.todos(username)
        return render_template('public/delete_task.html', lists = lists)

#striking a task done
@app.route('/done', methods = ['POST'])
def done():
    if request.method == 'POST':
        id = request.form['id']
        model.done(id)
        return redirect(url_for('home'))

#undo striking of task
@app.route('/undone', methods=['POST'])
def undone():
    id = request.form['id']
    model.undone(id)
    return redirect(url_for('home'))

#if users is already logged in then dashbboard otherwise homepage
@app.route('/schedule', methods = ['GET'])
def schedule():
    username = session['username']
    liststoday = model.todos_today(username)
    listsweek = model.todos_week(username)
    listsmonth = model.todos_month(username)
    return render_template('public/schedule.html', liststoday = liststoday, listsweek = listsweek, listsmonth = listsmonth)

#render about page
@app.route('/about', methods = ['GET'])
def about():
    return render_template('public/about.html')

#render terms of use page
@app.route('/terms', methods = ['GET'])
def terms():
    return render_template('public/terms.html')

#render privacy page
@app.route('/privacy', methods = ['GET'])
def privacy():
    return render_template('public/privacy.html')

##########ADMIN PAGE CODE BELOW##########

#check admins in database
user = ''
admin = model.check_admins()

#load admin from session to run befor each request
@app.before_request
def before_request_admin():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getadminsession')
def getadminsession():
    if 'user' in session:
        return session['user']
    return redirect(url_for('admin_home'))

#admin dashboard
@app.route('/admin', methods = ['GET'])
def admin_home():
    if 'user' in session:
        g.admin=session['user']
        signups = model.signups()
        signups24 = model.signups24()
        lists = model.lists()
        lists24 = model.lists24()
        return render_template('admin/dashboard.html', message = 'Welcome to your dashboard', signups = signups, signups24 = signups24, lists = lists, lists24 = lists24)
    return render_template('admin/homepage.html', message = 'Please login if you are the admin')

#redirecting to the home function above
@app.route('/admin-login', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        session.pop('user', None)
        areyouadmin = request.form['user']
        pwd = model.check_admin_pw(areyouadmin)
        if request.form['password'] == pwd:
            session['user'] = request.form['user']
            return redirect(url_for('admin_home'))
    return render_template('admin/homepage.html', message = 'Sorry, you are not the admin!')

#admin users page
@app.route('/users', methods = ['GET'])
def admin_users():
    users = model.all_users()
    return render_template('admin/users.html', users = users)

#a single user page
@app.route('/user-page', methods = ['GET', 'POST'])
def user_page():
    if request.method == 'POST':
        username = request.form['username']
        user = model.a_user(username)
        return render_template('admin/user_page.html', user = user)
    else:
        return render_template('admin/user_page.html')

#render the delete list page
@app.route('/delete-user', methods = ['POST'])
def delete_user():
        username = request.form['username']
        message = model.delete_user(username)
        return render_template('admin/delete_user.html', message = message)

#admin logout
@app.route('/admin-logout')
def admin_logout():
    session.pop('user')
    return redirect(url_for('admin_home'))

#Remove host and the website will be accessible at localhost:5000  
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = '5000', debug = True)

