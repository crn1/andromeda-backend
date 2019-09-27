from flask import jsonify

lang = {
    'en': {
        '201': 'Item is successfully created!',
        '400': 'Form format that you have provided is incorrect.',
        '401': 'You are either not logged in or you do not have user permission for this action.',
        '404': 'Page that yor are trying to reach does not exist.',
        '405': 'A request method is not supported for the requested resource.',
        '409': 'Item that you are trying to reach already exists.',
        '415': 'Filetype that you have provided is not allowed.',
        '500': 'There is an internal server error. This action cannot be taken.',

        'USER_LOGIN_SUCCESS':
            'Successfully logged in.',
        'USER_LOGIN_ALREADY_LOGGED_IN':
            'You are already logged in.',
        'USER_LOGIN_USER_DOES_NOT_EXIST':
            'E-mail that you have provided does not exists.',
        'USER_LOGIN_INCORRECT_PASSWORD':
            'Password that you have provided is incorrect.',

        'USER_LOGOUT_SUCCESS':
            'Successfully logged out!',

        'UNAUTHORIZED_FRESH_LOGIN_NEEDED':
            'Please re-login in order to access this page.',

        'POST_DELETE_NOT_AUTHOR':
            'You must be admin or author of this post in order to delete it.',
        'POST_PATCH_NOT_AUTHOR':
            'You must be admin or author of this post in order to patch it.',
        'POST_TOGGLE_PUBLISH_SUCCESS':
            'Post is published successfully!',

        'UNIVERSALS_PATCH_SUCCESS':
            'Item is successfully patched!',
        'UNIVERSALS_GET_SUCCESS':
            'Get query is successfully executed!',
        'UNIVERSALS_SEARCH_SUCCESS':
            'Search query is successfully executed!',
        'UNIVERSALS_DELETE_SUCCESS':
            'Item is successfully deleted.',
    }
}

def make_response(enum, status='success', langauge='en', data=None):
    return jsonify({
        'status': status,
        'message': lang[langauge][enum],
        'code': enum,
        'data': data,
    })
