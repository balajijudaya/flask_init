import os
import logging
import pymysql
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session

app = Flask(__name__)


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name_template=name)


"""
login, logout and welcome with cookies
commented now because doing the same with session is more secure
see below
"""
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("Successfully logged in.")
            response = make_response(redirect(url_for('welcome')))
            response.set_cookie('username', request.form.get('username'))
            return response
        else:
            error = "Incorrect username and/or password"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('username', '', expires=0)
    return response

@app.route('/')
def welcome():
    username = request.cookies.get('username')
    if username:
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('login'))
"""


"""
login, logout and welcome with session
Doint it with session is more secure than using cookies(see above)
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("Successfully logged in.")
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            app.logger.warning("Incorrect username and/or password for user {}"
            .format(request.form['username']))
            error = "Incorrect username and/or password"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))


def valid_login(username, password):
    # mysql
    MYSQL_DATABASE_HOST = os.getenv('IP', '0.0.0.0')
    MYSQL_DATABASE_USER = 'budayabanu'
    MYSQL_DATABASE_PASSWORD = ''
    MYSQL_DATABASE_DB = 'my_flask_app'
    
    conn = pymysql.connect(
        host=MYSQL_DATABASE_HOST,
        user=MYSQL_DATABASE_USER,
        passwd=MYSQL_DATABASE_PASSWORD,
        db=MYSQL_DATABASE_DB
        )
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user where username = '{}' AND password = '{}'"
    .format(username, password))
    
    data = cursor.fetchone()
    
    return data != None
    

if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=2)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    # app.secret_key = 'secret'
    # secret key generated using os.urandom(24) - more secure
    app.secret_key = '3\x04\xfc\xcd$H\x1fi\x7f;\xdai\xf8\xdcR\xbf\xac\xd4\x18\xea\xa3\xf2\xe0('
    app.run(host=host, port=port)
