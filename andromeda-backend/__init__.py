from flask import Flask, request, redirect, url_for
from .models import *
from .lang import make_response
from .secrets import secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
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

@app.errorhandler(400)
def incorrect_form(e):
    return make_response('400', 'error'), 400

@app.errorhandler(401)
def unauthorized(e):
    return make_response('401', 'error'), 401

@app.errorhandler(404)
def not_found(e):
    return make_response('404', 'error'), 404

@app.errorhandler(405)
def disallowed_method(e):
    return make_response('405', 'error'), 405

@app.errorhandler(409)
def conflict(e):
    return make_response('409', 'error'), 409

@app.errorhandler(415)
def wrong_filetype(e):
    return make_response('415', 'error'), 415

@app.errorhandler(500)
def internal_error(e):
    return make_response('500', 'error'), 500

from .user import user_bp
app.register_blueprint(user_bp)

#from .file import file_bp
#app.register_blueprint(file_bp)

from .post import post_bp
app.register_blueprint(post_bp)

from .category import category_bp as category_bp
app.register_blueprint(category_bp)

from .role import role_bp as role_blueprint
app.register_blueprint(role_blueprint)

from .user_role import user_role_bp
app.register_blueprint(user_role_bp)

#@app.route('/')
#def index():
#    return 'This is testing endpoint.'
