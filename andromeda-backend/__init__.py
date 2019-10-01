from flask import Flask, request, abort
from .models import *
from .secrets import secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

from flask_cors import CORS
cors = CORS(app,
    origins=['http://localhost:3000', 'http://localhost:3001'],
    headers=['Content-Type'],
    expose_headers=['Access-Control-Allow-Origin'],
    supports_credentials=True)

from flask_paranoid import Paranoid
Paranoid(app)

@app.before_request
def before_request():
    initialize_db()

@app.teardown_request
def teardown_request(exception):
    db.close()

@app.errorhandler(DoesNotExist)
def item_does_not_exists(e):
    return abort(404)

@app.errorhandler(ValueError)
def value_error(e):
    return abort(400)

from .user import user_bp
app.register_blueprint(user_bp)

#@app.route('/teapot')
#def teapot():
#    return ''
