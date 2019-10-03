from flask import Blueprint
from ..models.auth import UserRole, Role, User
from ..login_manager import role_required
from ..universals import create_or_patch, delete, get, search

blueprint = Blueprint('user_role', __name__, url_prefix='/userrole')

@blueprint.route('/<user_role_id>', methods=['GET'])
@role_required('ADMIN')
def get_category(user_role_id):
    return get(UserRole
            .select(UserRole, Role, User)
            .join(Role)
            .switch(UserRole)
            .join(User)
            .where(UserRole.id == int(user_role_id)), exclude=[User.password])

@blueprint.route('', methods=['GET'])
@role_required('ADMIN')
def search_user_roles():
    return search(UserRole, exclude_fields=[User.password])

@blueprint.route('', methods=['POST'])
@blueprint.route('/<user_role_id>', methods=['PATCH'])
@role_required('ADMIN')
def patch_or_create_user_role(user_role_id=-1):
    return create_or_patch(UserRole, user_role_id)

@blueprint.route('/<user_role_id>', methods=['DELETE'])
@role_required('ADMIN')
def delete_user_role(user_role_id):
    return delete(UserRole, user_role_id)
