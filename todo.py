#import the model file making sure the name is unique
#g is global variable for flask
from flask import Flask, render_template, request, session, redirect, url_for, g
import model

#set secret key
app = Flask(__name__)
app.config.from_pyfile('config.py')

#check users in database
username = ''
user = model.check_users()

#home or root page
@app.route('/', methods = ['GET'])
def home():
    if 'username' in session:
        g.user=session['username']
        lists = model.todos(username)
        return render_template('dashboard.html', lists = lists)
    return render_template('homepage.html', message = 'Login or sign up!')

#redirecting to the home function above
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None)
        areyouuser = request.form['username']
        pwd = model.check_pw(areyouuser)
        if request.form['password'] == pwd:
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('homepage.html')

#load user from session to run befor each request
@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

#define user signup
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        message = 'Please sign up!'
        return render_template('signup.html', message = message)
    else:
        username = request.form['username']
        password = request.form['password']
        message = model.signup(username, password)
        return render_template('signup.html', message = message)

@app.route('/getsession')
def getsession():
    if 'username' in session:
        return session['username']
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('home'))

#render a users dashboard
@app.route('/dashboard', methods = ['GET'])
def dashboard():
    try:
        username = session['username']
        lists = model.todos(username)
        return render_template('dashboard.html', lists = lists)
    except:
        return render_template('homepage.html', message = "Please sign in to access your dashboard")

#render the create new list or task page
@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        content = request.form['content']
        message = model.create(username, title, content)
        return render_template('create.html', message = message )
    else:
        return render_template('create.html')

#render the edit list name page
@app.route('/edit-title', methods = ['GET', 'POST'])
def edit_title():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        new_title = request.form['new_title']
        message = model.edit_title(username, title, new_title)
        return render_template('edit_title.html', message = message )
    else:
        return render_template('edit_title.html')

#render the edit task page
@app.route('/edit-task', methods = ['GET', 'POST'])
def edit_task():
    if request.method == 'POST':
        content = request.form['content']
        new_content = request.form['new_content']
        message = model.edit_task(content, new_content)
        return render_template('edit_task.html', message = message )
    else:
        return render_template('edit_task.html')

#render the delete list page
@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        message = model.delete(username, title)
        return render_template('delete.html', message = message )
    else:
        return render_template('delete.html')

#render the delete a task page
@app.route('/delete-task', methods = ['GET', 'POST'])
def delete_task():
    if request.method == 'POST':
        content = request.form['content']
        title = request.form['title']
        message = model.delete_task(content, title)
        return render_template('delete_task.html', message = message )
    else:
        return render_template('delete_task.html')

#about page
@app.route('/about', methods = ['GET'])
def about():
    return render_template('about.html')

#terms of use page
@app.route('/terms', methods = ['GET'])
def terms():
    return render_template('terms.html')

#privacy page
@app.route('/privacy', methods = ['GET'])
def privacy():
    return render_template('privacy.html')
              
if __name__ == '__main__':
    app.run(port = '5000', debug = True)