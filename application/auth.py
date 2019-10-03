from flask import Blueprint, request
from playhouse.shortcuts import model_to_dict
from .models.auth import User, UserRole, Role
from flask_login import current_user, login_user, logout_user, login_required
from .login_manager import bcrypt

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return (403, 'USER_ALREADY_LOGGED_IN')

    email = request.form['email']
    password = request.form['password']
    remember = request.form['remember']
    user = User.get(User.email == email)
    if bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=remember)
        data = model_to_dict(user, exclude=[User.password])

        if current_user.has_role('ADMIN'):
            data['roles'] = current_user.get_roles()
        else:
            data['roles'] = []

        return data

    return abort(401, 'INCORRECT_PASSWORD')

@blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return 'Successfully logged out!'
