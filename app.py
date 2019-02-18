'''
This scripts runs the application using a development server
It contains the definition of routes and views for the application
'''

from flask import Flask
app = Flask(__name__)

#Make the WSGI interface avaiable at the level so wfastcgi get it
wsgi_app = app.wsgi_app

#Import all of our routes from routes.py
from routes import *;


#Launching our server
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_HOST', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)