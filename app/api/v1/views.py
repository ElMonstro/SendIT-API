from flask import request
from flask_restful  import Resource
from app.api.v1.models import ParcelOrders, Validator, Users
import jwt
import datetime
from instance.config import DevelopmentConfig
from functools import wraps

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
            except:
                return {message: 'Invalid token'}, 401
            return f(*args, **kwargs, user_data=user_data)
        else:
            return {message: 'Token missing'}, 401       
        
    return wrapper




class Parcels(Resource):
    """Handles requests for the /parcels route"""

    def __init__(self):
        self.db = ParcelOrders()
    
    @authenticate
    def get(self, user_data):
        if user_data['is_admin']:
            return self.db.get_all_orders()
        else: 
            return { message: 'Cannot perform this operation' }, 401

    @authenticate  
    def post(self, user_data):
        if user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        data = request.get_json()
        data_list = data['order']
        success = self.db.save(data_list)

        if success:       
            return {message: 'Order created'}, 201
        else:
            return {message: 'Invalid data format'}, 400


class Parcel(Resource):
    """Handles request for /parcels/<id> route"""

    def __init__(self):
        self.db = ParcelOrders()

    @authenticate
    def get(self, id, user_data):
        try:
            int_id = int(id)
        except:
            return {message: 'Wrong id format'}, 400

        order = self.db.get_specific_order(int_id)

        if order:
            return order
        else: 
            return {message: 'No Parcel delivery order with that id'}, 400
        
    @authenticate
    def put(self, id, user_data):
        if not user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        try:
            int_id = int(id)
        except:
            return {message: 'Wrong id format'}, 400

        success = self.db.change_delivery_status(int_id)

        if success:
            return {message: 'Status changed'} 
        else:       
            return {message: 'No Parcel delivery order with that id'}, 400


class UserParcels(Resource):
    """Handles the route /users/<user_id>/parcels"""
    
    def __init__(self):
        self.db = ParcelOrders()

    @authenticate
    def get(self, id, user_data):        

        try:
            int_id = int(id)
        except:
            return {message: 'Wrong id format'}, 400

        if not user_data['user id'] == int(id):
            return { message: 'Cannot perform this operation' }, 401

        orders = self.db.get_all_user_orders(int_id)

        if not  orders:
            return {message: 'No orders by that user'}, 400
        return orders

            


class CancelOrder(Resource):
    """Handles the route /parcels/<parcel_id>/cancel"""

    def __init__(self):
        self.db = ParcelOrders()

    @authenticate
    def put(self, id, user_data):
        if user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        try:
            int_id = int(id)
        except:
            return {message: 'Wrong id format'}, 400

        success = self.db.cancel_order(int_id)

        if success:
            return {message: 'Order canceled'} 
        else:       
            return {message: 'No Parcel delivery order with that id'}, 400

class Login(Resource):
    """Handles the route /login"""

    def __init__(self):
        self.auth = request.get_json()
        self.validator = Validator()
        self.users = Users()

    def post(self):
        if self.auth:
            email = self.auth['email']
            password = self.auth['password']
            user_id = self.validator.user_checker(email)            
            # If user is not registered
            if not user_id:
                return {message: 'User email not found'}, 401

            is_admin = self.users.is_admin(user_id)

            isValid = self.validator.password_checker(user_id, password)
            # If password is valid
            if isValid:
                exp = datetime.datetime.utcnow() + datetime.timedelta(hours=24*7)
                payload = {'user id': user_id, 'email': email,'is_admin': is_admin, 'exp': exp}
                token = jwt.encode(payload, key=secret, ) 
                return {message: 'You have been logged in',
                'token': token.decode('utf-8',)}
            # If password not valid
            return {message: 'Invalid password'}, 401
        # If there is no authentication information
        return {message: 'Email and password required'}, 401






