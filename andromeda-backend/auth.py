from .models import *
from . import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_login import LoginManager, current_user
from functools import wraps
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)

def role_required(role='NONE'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            user_role = (UserRole
                        .select()
                        .join(Role)
                        .switch(UserRole)
                        .join(User)
                        .where(
                            (User.id == current_user.id) &
                            ((Role.name == role) | (Role.name == 'ADMIN'))
                        ))
            if not user_role:
                return login_manager.unauthorized()

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    user = User.get_by_id(int(user_id))
    if user:
        return user
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return abort(401)

@login_manager.needs_refresh_handler
def refresh():
    return abort(401, 'FRESH_LOGIN_NEEDED')
