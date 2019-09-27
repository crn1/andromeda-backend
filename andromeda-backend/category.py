from flask import Blueprint, request, abort
from .models import *
from .lang import make_response
from .auth import role_required
from .universals import create_or_patch, delete, get, search

category_bp = Blueprint('category_bp', __name__, url_prefix='/category')

@category_bp.route('/<category_id>', methods=['GET'])
def get_category(category_id):
    return get(Category.get_by_id(int(category_id)))

@category_bp.route('', methods=['GET'])
def search_categories():
    return search(Category, search_fields=[Category.name])

@category_bp.route('/<category_id>', methods=['DELETE'])
@role_required('ADMIN')
def delete_category(category_id):
    return delete(Category, category_id, True)

@category_bp.route('', methods=['POST'])
@category_bp.route('/<category_id>', methods=['PATCH'])
@role_required('ADMIN')
def create_or_patch_category(category_id=-1):
    return create_or_patch(Category, category_id)
