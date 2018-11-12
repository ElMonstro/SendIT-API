import jwt
import datetime
from functools import wraps
from app.api.v1.mock_data import message
from flask import request, current_app as app


# Authentication decorator
def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'token' in request.headers:
            token = request.headers.get('token')
            try:
                user_data = jwt.decode(token, key=app.config['SECRET'], algorithms='HS256')
            except jwt.ExpiredSignatureError:# Add test
                return {message: 'Token expired, login again'}, 401
            except jwt.InvalidTokenError:
                return {message: 'Invalid token'}, 401
            
            return f(*args, **kwargs, user_data=user_data)
        else:
            return {message: 'Token missing'}, 401       
        
    return wrapper
