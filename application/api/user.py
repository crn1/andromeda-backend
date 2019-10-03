from flask import Blueprint, request, abort
from flask_login import login_required, fresh_login_required, current_user, logout_user
from ..models.auth import User
from ..login_manager import bcrypt, role_required
from ..universals import create_or_patch, delete, get, search

from playhouse.shortcuts import model_to_dict

blueprint = Blueprint('user', __name__, url_prefix='/user')

@blueprint.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_by_id(int(user_id))
    data = model_to_dict(user, exclude=[User.password])

    if current_user.is_authenticated:
        if current_user.has_role('ADMIN') or current_user.id == int(user_id):
            data['roles'] = user.get_roles()

    return data

@blueprint.route('', methods=['GET'])
@role_required('ADMIN')
def search_users():
    return search(User,
                search_fields=[User.fullname, User.email, User.description],
                exclude_fields=[User.password])

@blueprint.route('', methods=['POST'])
@blueprint.route('/<user_id>', methods=['PATCH'])
@fresh_login_required
def create_or_patch_user(user_id=-1):
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

@blueprint.route('/<user_id>', methods=['DELETE'])
@role_required('ADMIN')
def delete_user(user_id):
    if current_user.id == int(user_id):
        logout_user()
    return delete(User, user_id, True)
