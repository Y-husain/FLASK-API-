"""Decorator for Authentication."""
from functools import wraps
from flask import request
import jwt
import os


def token_required(f):
    """Decorate to check if valid token present in request header."""

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """Wrap the function."""
        token = None

        if 'access_token' in request.headers:
            token = request.headers['access_token']

        # Verifies token is present
        if not token:
            return {'Message': "Unauthorized, access token required!"}, 401
        try:
            # try to decode using token and secret key
            payload = jwt.decode(token, os.getenv('SECRET'))
            current_user = payload['sub']
        except jwt.ExpiredSignature:
            return {'Message': 'Expired token. Please log in.'}
        except jwt.InvalidTokenError:
            return {'Message': 'Invalid token. Please register or log in'}

        return f(self, current_user, *args, **kwargs)

    return wrapper