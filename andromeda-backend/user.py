from flask import Blueprint, request, abort
from .models import *
from .lang import make_response
from .auth import bcrypt, role_required
from flask_login import login_required, fresh_login_required, current_user, login_user, logout_user
from .universals import create_or_patch, delete, get, search
from playhouse.shortcuts import model_to_dict

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

@user_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return make_response('USER_LOGIN_ALREADY_LOGGED_IN', 'error')

    try:
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

            return make_response('USER_LOGIN_SUCCESS', data=data)

        return make_response('USER_LOGIN_INCORRECT_PASSWORD', 'error')

    except DoesNotExist:
        return make_response('USER_LOGIN_USER_DOES_NOT_EXIST', 'error')

@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return make_response('USER_LOGOUT_SUCCESS')

@user_bp.route('/current', methods=['GET'])
@login_required
def current():
    data = model_to_dict(current_user, exclude=[User.password])
    data['roles'] = current_user.get_roles()
    return make_response('UNIVERSALS_GET_SUCCESS', data=data)

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.get_by_id(int(user_id))
        data = model_to_dict(user, exclude=[User.password])

        if current_user.is_authenticated:
            if current_user.has_role('ADMIN') or current_user.id == int(user_id):
                data['roles'] = user.get_roles()

        return make_response('UNIVERSALS_GET_SUCCESS', data=data)

    except:
        abort(404)

@user_bp.route('', methods=['GET'])
@role_required('ADMIN')
def search_users():
    return search(User,
                search_fields=[User.fullname, User.email, User.description],
                exclude_fields=[User.password])

@user_bp.route('', methods=['POST'])
@user_bp.route('/<user_id>', methods=['PATCH'])
@fresh_login_required
def patch_user(user_id=-1):
    if current_user.id == int(user_id) or current_user.has_role('ADMIN'):
        return create_or_patch(User,
                            user_id,
                            conversion_dict={
                                'password': {
                                    'func': bcrypt.generate_password_hash,
                                }
                            })
    else:
        return abort(401)

@user_bp.route('/<user_id>', methods=['DELETE'])
@role_required('ADMIN')
def delete_user(user_id):
    if current_user.id == int(user_id):
        logout_user()
    return delete(User, user_id, True)
