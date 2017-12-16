import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# __name__ will be __main__ if invoked from the terminal
if __name__ == '__main__':
    """
    env variables 'IP' and 'PORT' are needed only to run the flask app in cloud9
    and they are preset by cloud9.
    """
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port)
