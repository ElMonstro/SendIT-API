from flask import request
from flask_restful  import Resource
import jwt
import datetime
from instance.config import DevelopmentConfig
from functools import wraps
from app.api.utils.validators import Validator
from app.api.v2.models.user_models import Users

secret = DevelopmentConfig.SECRET

message = 'message'


# Authentication decorator
def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'token' in request.headers:
            token = request.headers.get('token')
            try:
                user_data = jwt.decode(token, key=secret, algorithms='HS256')
            except jwt.ExpiredSignatureError:# Add test
                return {message: 'Token expired, login again'}, 401
            except jwt.InvalidTokenError:
                return {message: 'Invalid token'}, 401
            
            return f(*args, **kwargs, user_data=user_data)
        else:
            return {message: 'Token missing'}, 401       
        
    return wrapper


class Login(Resource):
    """Handles the route /login"""

    def __init__(self):
        self.auth = request.get_json()
        self.validator = Validator()
        self.users = Users()

    def post(self):
        """Handles POST request to /auth/signin"""
        message_dict = {message: 'Username and password required'}
        status_code = 400
        if self.auth:
            try:
                username = self.auth['username']                
            except TypeError:
                return {message: 'Invalid data format'}, 400
            except KeyError:
                return {message: 'Username not provided'}, 400
            
            try:
                password = self.auth['password']                
            except TypeError:
                return {message: 'Invalid data format'}, 400
            except KeyError:
                return {message: 'Password not provided'}, 400
               
            # If user is not registered
            user_id = self.users.is_user_there(username)
            if not user_id:
                return {message: 'User not registered'}, 401

            # If user is admin
            is_admin = self.users.is_admin(username) 

            is_valid = self.users.check_password(username, password)
            # If password is valid
            if is_valid:
                exp = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                payload = {'user id': user_id, 'username': username,'is_admin': is_admin, 'exp': exp}
                token = jwt.encode(payload, key=secret, ) 
                return {
                'token': token.decode('utf-8',)}
            # If password not valid
            message_dict = {message: 'Invalid password'}
            status_code = 401
        # If there is no authentication information
        return message_dict, status_code

