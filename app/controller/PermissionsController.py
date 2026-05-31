from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def login_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return decorator


def reqrole(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            role = get_jwt().get("role")

            if role not in roles:
                return jsonify({"error": "Accès refusé"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper