from flask import Flask, request, abort

#===============================
# General configuration
#===============================

# secrets.py file is generated by running /install/development.sh script
from .secret_key import secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

#===============================
# Security options and functions
#===============================
from flask_cors import CORS

cors = CORS(app,
    origins=['http://localhost:3000', 'http://localhost:3001'],
    headers=['Content-Type'],
    expose_headers=['Access-Control-Allow-Origin'],
    supports_credentials=True)

from flask_paranoid import Paranoid
Paranoid(app)

#===============================
# Database options and functions
#===============================
from .models.auth import User, UserRole, Role
from .models.blog import Post, Category
from .database import database

@app.before_request
def before_request():
    database.connect()
    database.create_tables([User, Role, UserRole,
                            Category, Post], safe=True)

@app.teardown_request
def teardown_request(exception):
    database.close()

#===============================
# Error handlers
#===============================
from peewee import DoesNotExist

@app.errorhandler(DoesNotExist)
def item_does_not_exists(e):
    return abort(404)

@app.errorhandler(KeyError)
def request_error(e):
    return abort(400)

@app.errorhandler(ValueError)
def value_error(e):
    return abort(400)

#===============================
# Blueprint imports
#===============================
from .auth import blueprint as auth_bp
app.register_blueprint(auth_bp)

from .api.user import blueprint as user_bp
app.register_blueprint(user_bp)

from .api.role import blueprint as role_bp
app.register_blueprint(role_bp)

from .api.user_role import blueprint as user_role_bp
app.register_blueprint(user_role_bp)

#===============================
# __name__ == '__main__'
#===============================
if __name__ == '__main__':
    app.run(host='0.0.0.0')
