import os
from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'
    
@app.route('/geturl')
def get_url():
    return url_for('show_user_profile', username='chitra')
    
@app.route('/hello')
def hello_world():
    # To debug step by step - pdb
    # import pdb; pdb.set_trace()
    return 'Hello World!'

@app.route('/user/<username>')
def show_user_profile(username):
    """
    show the user profile for that username
    """
    return "User {}".format(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "Post %d" %post_id
    
# __name__ will be __main__ if invoked from the terminal
if __name__ == '__main__':
    """
    env variables 'IP' and 'PORT' are needed only to run the flask app in cloud9
    and they are preset by cloud9.
    """
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    # Don't set debug to True in production
    app.debug = True
    app.run(host=host, port=port)
