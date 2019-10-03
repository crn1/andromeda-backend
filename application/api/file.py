from flask import Blueprint, session, request, send_from_directory, abort
from .models import *
from .lang import make_response
from .auth import login_manager, role_required
from werkzeug.utils import secure_filename
import os
import uuid
from .universals import search

file_bp = Blueprint('file', __name__, url_prefix='/file')

ROOT_DIR = os.path.dirname(os.path.realpath('__file__'))
UPLOAD_DIR = os.path.join(ROOT_DIR, 'files')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_bp.route('/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@file_bp.route('', methods=['GET'])
def search_files():
    return search(File, search_fields=[File.description, File.filename])

@file_bp.route('', methods=['POST'])
@role_required('AUTHOR')
def upload_file():
    if 'description' not in request.form or 'file' not in request.files:
        return abort(400)

    file = request.files['file']
    description = request.form['description']
    if file.filename == '':
        return abort(400)

    filename = secure_filename(file.filename)
    if file and allowed_file(filename):

        uuid_filename = str(uuid.uuid4().hex) + str(os.path.splitext(filename)[1])
        try:
            file.save(os.path.join(UPLOAD_DIR, uuid_filename))
            upload_to_database(uuid_filename, description)
            return make_response('201'), 201
        except:
            return abort(500)

    return abort(415)

def upload_to_database(filename, description):
    file = File.create(
        filename=filename,
        description=description)
    file.save()

@file_bp.route('/<filename>', methods=['DELETE'])
@role_required('AUTHOR')
def delete_file(filename):
    filename = secure_filename(filename)

    try:
        os.remove(os.path.join(UPLOAD_DIR, filename))
        delete_from_database(filename)
    except FileNotFoundError:
        return abort(404)
    except:
        abort(500)

    return make_response('UNIVERSALS_DELETE_SUCCESS')

def delete_from_database(filename):
    file = File.get(File.filename == filename)
    file.delete_instance(recursive=True)
