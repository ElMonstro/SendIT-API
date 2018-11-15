import jwt
import datetime
from functools import wraps
from flask import request, current_app as app

message = 'message'

# Authentication decorator
def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'token' in request.headers:
            token = request.headers.get('token')
            try:
                data = jwt.decode(token, key=app.config['SECRET'], algorithms='HS256')
            except jwt.ExpiredSignatureError:# Add test
                return {message: 'Token expired, login again'}, 401
            except jwt.InvalidTokenError:
                return {message: 'Invalid token'}, 401
            
            return f(*args, **kwargs, user_id=data['user_id'])
        else:
            return {message: 'Token missing'}, 401       
        
    return wrapper
