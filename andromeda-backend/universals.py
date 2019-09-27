from flask import request, abort
from flask_login import current_user
from .models import *
from .lang import make_response
from playhouse.shortcuts import model_to_dict, dict_to_model

def get(query, exclude=[]):
    try:
        data = model_to_dict(query, exclude=exclude)
        return make_response('UNIVERSALS_GET_SUCCESS', data=data)

    except Exception as e:
        return str(e)
        abort(404)

def search(resource_class, search_fields=[], exclude_fields=[]):
    limit = 10
    page = 1
    search = ''
    # order_by = 'id'

    try:
        if 'limit' in request.args:
            limit = int(request.args['limit'])
        if 'page' in request.args:
            page = int(request.args['page'])
        if 'search' in request.args:
            search = request.args['search']
        # if 'order_by' in request.args:
        #     search = request.args['order_by']
        if limit > 30:
            limit = 30
        if limit < 0:
            limit = 5

        query = resource_class.select()

        data = {}
        data['total_prefiltered'] = query.count()

        for field in search_fields:
            query = query.orwhere(field.contains(search))

        if resource_class == Post:
            if current_user.is_authenticated:
                if current_user.has_role('ADMIN'):
                    query = query.where(Post.author_id == current_user.id)
            else:
                query = query.where(Post.is_published == True)


        query = query.paginate(page, limit)

        data['items'] = []
        for item in query:
            data_to_append = model_to_dict(item, exclude=exclude_fields)

            if resource_class == User:
                data_to_append['roles'] = item.get_roles()

            data['items'].append(data_to_append)

        data['total_filtered'] = query.count()
        return make_response('UNIVERSALS_SEARCH_SUCCESS', data=data)

    except ValueError:
        abort(400)
    except:
        abort(500)

def create_or_patch(resource_class, resource_id=None, conversion_dict={}, exclude_args=[]):
    args_dict = request.get_json(silent=True)
    if not args_dict:
        abort(400)

    try:
        if request.method == 'POST':
            resource_instance = resource_class.create(**args_dict)
        else:
            resource_instance = resource_class.get_by_id(int(resource_id))

        for arg in conversion_dict:
            if arg in args_dict:
                try:
                    field_target = conversion_dict[arg]['field_target']
                except:
                    field_target = arg

                exclude_args.append(field_target)

                func = conversion_dict[arg]['func']
                new_arg = func(args_dict[arg])
                setattr(resource_instance, field_target, new_arg)

        for arg in args_dict:
            if not arg in exclude_args:
                setattr(resource_instance, arg, args_dict[arg])

        data=model_to_dict(resource_instance, exclude=[User.password])
        resource_instance.save()

        if(request.method == 'POST'):
            return make_response('201', data=data), 201
        else:
            return make_response('UNIVERSALS_PATCH_SUCCESS', data=data)

    except DoesNotExist:
        return abort(404)
    except:
        return abort(500)

def delete(resource_class, resource_id, recursive=False):
    try:
        resource_instance = resource_class.get_by_id(int(resource_id))
        resource_instance.delete_instance(recursive=recursive)
        return make_response('UNIVERSALS_DELETE_SUCCESS')

    except DoesNotExist:
        return abort(404)
    except:
        return abort(500)
