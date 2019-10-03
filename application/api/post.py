from flask import Blueprint, request, abort
from .models import *
from .auth import role_required
from .universals import create_or_patch, delete, get, search
from flask_login import current_user, login_required
from slugify import slugify
from playhouse.shortcuts import model_to_dict

post_bp = Blueprint('post', __name__, url_prefix='/post')

def get_author_id(author_id):
    if current_user.has_role('ADMIN'):
        return author_id
    return current_user.id

@post_bp.route('/<slug>', methods=['GET'])
def get_post(slug):
    return get(Post
                .select(Post, Category)
                .join(Category)
                .where(
                    (Post.slug == slug) &
                    (Post.is_published == True)).get(), [User.password])

@post_bp.route('/id/<post_id>', methods=['GET'])
@login_required
def get_post_by_id(post_id):
    post = Post.get_by_id(int(post_id))

    if current_user.id == post.author_id or current_user.has_role('ADMIN'):
       return get(post, exclude=[User.password])
    else:
        return abort(401)

@post_bp.route('', methods=['GET'])
def search_posts():
    return search(Post,
                search_fields=[Post.title, Post.content, Post.description],
                exclude_fields=[User.password, Post.content])

@post_bp.route('/<post_id>', methods=['DELETE'])
@role_required('AUTHOR')
def delete_post(post_id):
    post = Post.get_by_id(int(post_id))

    if current_user.id == post.author_id or current_user.has_role('ADMIN'):
       return delete(Post, post_id)
    else:
        return abort(401)

@post_bp.route('', methods=['POST'])
@post_bp.route('/<post_id>', methods=['PATCH'])
@role_required('AUTHOR')
def create_or_patch_post(post_id=-1):
    if request.method == 'PATCH':
        post = Post.get_by_id(int(post_id))
        if not current_user.id == post.author_id and not current_user.has_role('ADMIN'):
            return abort(401, 'NOT_AUTHOR')

    return create_or_patch(Post,
                post_id,
                conversion_dict={
                    'title': {
                        'func': slugify,
                        'field_target': 'slug',
                    },
                    'author_id': {
                        'func': get_author_id,
                    },
                },
                exclude_args = [] if
                    current_user.has_role('ADMIN')
                    else ['is_published'])


@post_bp.route('/<post_id>/toggle_publish', methods=['GET'])
@role_required('ADMIN')
def publish_post(post_id):
    post = Post.get_by_id(post_id)

    if post.is_published:
        post.is_published = False
    else:
        post.is_published = True

    post.save()

    return model_to_dict(post, exclude=[User.password, Post.content])
