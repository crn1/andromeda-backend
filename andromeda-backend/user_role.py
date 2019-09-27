from flask import Blueprint, request, abort
from .models import *
from .lang import make_response
from .auth import role_required
from playhouse.shortcuts import model_to_dict
from .universals import create_or_patch, delete, get, search

user_role_bp = Blueprint('user_role_bp', __name__, url_prefix='/userrole')

@user_role_bp.route('/<user_role_id>', methods=['GET'])
@role_required('ADMIN')
def get_category(user_role_id):
    return get(UserRole
            .select(UserRole, Role, User)
            .join(Role)
            .switch(UserRole)
            .join(User)
            .where(UserRole.id == int(user_role_id)), exclude=[User.password])

@user_role_bp.route('', methods=['GET'])
@role_required('ADMIN')
def search_user_roles():
    return search(UserRole, exclude_fields=[User.password])

@user_role_bp.route('', methods=['POST'])
@user_role_bp.route('/<user_role_id>', methods=['PATCH'])
@role_required('ADMIN')
def patch_or_create_user_role(user_role_id=-1):
    return create_or_patch(UserRole, user_role_id)

@user_role_bp.route('/<user_role_id>', methods=['DELETE'])
@role_required('ADMIN')
def delete_user_role(user_role_id):
    return delete(UserRole, user_role_id)
