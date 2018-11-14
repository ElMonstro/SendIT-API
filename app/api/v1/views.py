from flask import request, current_app as app
from flask_restful import Resource
from app.api.v1.models import ParcelOrders, Validator, Users
from app.api.utils.auth_decorator import authenticate
import datetime
import jwt

message = 'message'


class Parcels(Resource):
    """Handles requests for the /parcels route"""

    def __init__(self):
        self.db = ParcelOrders()

    @authenticate
    def get(self, user_data):
        if user_data['is_admin']:
            return {message: 'All orders fetched',
                'orders': self.db.get_all_orders()}, 200
        else:
            return {message: 'Cannot perform this operation'}, 401

    @authenticate
    def post(self, user_data):
        message_dict = {}
        status_code = 200
        if user_data['is_admin']:
            return {message: 'Cannot perform this operation'}, 401

        data = request.get_json()
        order = self.db.save(data, user_data['user id'])

        if not message in order:
            message_dict = {message: 'Order created',
            'order': order}
            status_code = 201
        else:
            message_dict = order
            status_code = 400
        return message_dict, status_code


class Parcel(Resource):
    """Handles request for /parcels/<id> route"""

    def __init__(self):
        self.db = ParcelOrders()

    @authenticate
    def get(self, id, user_data):
        message_dict = {}
        status_code = 200
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        order = self.db.get_specific_order(int_id)

        if order:
          return {message: 'One order fetched', 'order': order}
    
        else:
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 400
        return message_dict, status_code

    @authenticate
    def put(self, id, user_data):
        message_dict = {}
        status_code = 200
        if not user_data['is_admin']:
            return {message: 'Cannot perform this operation'}, 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        order = self.db.change_delivery_status(int_id)

        if order:
            message_dict = {message: 'Status changed',
            'order': order}
        else:
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 400
        return message_dict, status_code


class UserParcels(Resource):
    """Handles the route /users/<user_id>/parcels"""

    def __init__(self):
        self.db = ParcelOrders()

    @authenticate
    def get(self, id, user_data):
        message_dict = {message: 'Cannot perform this operation'}
        status_code = 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        if user_data['user id'] == int(id) or user_data['is_admin']:
            orders = self.db.get_all_user_orders(int_id)
            if not orders:
                return {message: 'No orders by that user'}, 400
            return {message: 'User orders fetched', 'order': orders}
        # If user not admin or his/her id is not equal to the user id are  trying to access
        return message_dict, status_code


class CancelOrder(Resource):
    """Handles the route /parcels/<parcel_id>/cancel"""

    def __init__(self):
        self.db = ParcelOrders()

    @authenticate
    def put(self, id, user_data):
        message_dict = {}
        status_code = 200
        if user_data['is_admin']:
            return {message: 'Cannot perform this operation'}, 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        order = self.db.cancel_order(int_id)

        if order:
            message_dict = {message: 'Order canceled', 'order': order}
        else:
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 400
        return message_dict, status_code


class Login(Resource):
    """Handles the route /login"""

    def __init__(self):
        self.auth = request.get_json()
        self.validator = Validator()
        self.users = Users()

    def post(self):
        message_dict = {message: 'Email and password required'}
        status_code = 400
        if self.auth:
            try:
                email = self.auth['email']
            except TypeError:
                return {message: 'Invalid data format'}, 400
            except KeyError:
                return {message: 'Email not provided'}, 400

            try:
                password = self.auth['password']
            except TypeError:
                return {message: 'Invalid data format'}, 400
            except KeyError:
                return {message: 'Password not provided'}, 400

            user_id = self.validator.user_checker(email)
            # If user is not registered
            if not user_id:
                return {message: 'User email not found'}, 401

            # If user is admin
            is_admin = self.users.is_admin(user_id)

            isValid = self.validator.password_checker(user_id, password)
            # If password is valid
            if isValid:
                exp = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                payload = {'user id': user_id, 'email': email,
                           'is_admin': is_admin, 'exp': exp}
                token = jwt.encode(payload, key=app.config['SECRET'], )
                return {
                    'token': token.decode('utf-8',)}
            # If password not valid
            message_dict = {message: 'Invalid password'}
            status_code = 401
        # If there is no authentication information
        return message_dict, status_code
