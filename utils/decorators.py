import jwt
from flask import request, abort

from utils.constants import JWT_SECRET_KEY, JWT_ALGORITHM


def auth_required(func):
    """
    Check authorization token for authentication \n
    :param func: function for checking
    """
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers.get('Authorization')
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except Exception:
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """
    Check authorization token for admin authentication \n
    :param func: function for checking
    """
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers.get('Authorization')
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except Exception:
            abort(401)

        user = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        role = user.get('role')

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper
