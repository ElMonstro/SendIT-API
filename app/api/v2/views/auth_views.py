from werkzeug.security import generate_password_hash
from validate_email import validate_email
from flask import request
from flask_restful  import Resource
import jwt
import datetime
from config import Config
from functools import wraps
from app.api.v2.utils.validators import Validator
from app.api.v2.models.user_models import Users

secret = Config.SECRET

message = 'message'


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
            user_id = self.users.get_user_id(username)
            if not user_id:
                return {message: 'User not registered'}, 401

            is_valid = self.users.check_password(username, password)
            # If password is valid
            if is_valid:
                exp = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                payload = {'user_id': user_id[0], 'exp': exp}
                token = jwt.encode(payload, key=secret, ) 
                return {
                'token': token.decode('utf-8',)}
            # If password not valid
            message_dict = {message: 'Invalid password'}
            status_code = 401
        # If there is no authentication information
        return message_dict, status_code


class Register(Resource):
    """Register users"""
    def __init__(self):
        self.auth = request.get_json()
        self.validator = Validator()
        self.users = Users()
    
    def post(self):
        try:
            username = self.auth['username']                
        except TypeError:
            return {message: 'Invalid data format'}, 400
        except KeyError:
            return {message: 'Username not provided'}, 400  
        try:
            password = self.auth['password']               
        except KeyError:
            return {message: 'Password not provided'}, 400          
        try:
            email = self.auth['email']                
        except KeyError:
            return {message: 'Email not provided'}, 400

        usernames_emails = self.users.get_all_username_emails()
        response = self.validator.username_email_validator(username, email,usernames_emails)
        # Check if email and password are valid
        if response != True:
            return {message: response}, 400

        is_valid = self.validator.password_validator(password)
        if is_valid != True: 
            return {message: is_valid}, 400
       
        password = generate_password_hash(password)
        user_dict = {'username': username, 'password': password, 'email': email}
        user_id = self.users.add_user(user_dict)
        user_dict['user_id'] = user_id
        del user_dict['password']
        return {
            message: 'User registered',
            'user': user_dict
            }
