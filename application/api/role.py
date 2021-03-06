from flask import Blueprint
from ..models.auth import Role
from ..login_manager import role_required
from ..universals import search

blueprint = Blueprint('role', __name__, url_prefix='/role')

#@role_bp.route('/<role_id>', methods=['GET'])
#def get_role(role_id):
#    return get(Role.get_by_id(int(role_id)))

@blueprint.route('', methods=['GET'])
def search_roles():
    return search(Role, search_fields=[Role.name])

#@role_bp.route('', methods=['POST'])
#@role_bp.route('/<role_id>', methods=['PATCH'])
#@role_required('AUTHOR')
#def patch_role(role_id=-1):
#    return create_or_patch(Role, role_id)
#
#@role_bp.route('/<role_id>', methods=['DELETE'])
#@role_required('ADMIN')
#def delete_role(role_id):
#    return delete(Role, role_id, True)
