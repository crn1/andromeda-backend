from flask import Blueprint, request, abort
from .models import *
from .lang import make_response
from .auth import role_required
from playhouse.shortcuts import model_to_dict
from .universals import create_or_patch, delete, get, search

role_bp = Blueprint('role_bp', __name__, url_prefix='/role')

#@role_bp.route('/<role_id>', methods=['GET'])
#def get_role(role_id):
#    return get(Role.get_by_id(int(role_id)))

@role_bp.route('', methods=['GET'])
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
