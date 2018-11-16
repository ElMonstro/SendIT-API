from flask import request
from flask_restful  import Resource
from app.api.v2.models.order_models import Orders
import jwt
import datetime
from instance.config import DevelopmentConfig
from functools import wraps
from app.api.v2.utils.auth_decorator import authenticate
from app.api.v2.utils.validators import Validator

message = 'message'


class Parcels(Resource):
    """Handles requests for the /parcels route"""

    def __init__(self):
        self.orders = Orders() 

    
    @authenticate
    def get(self, user_data):        
        if user_data['is_admin']:
            orders = self.orders.get_all_orders()
            return {message: "All orders fetched", 'orders': orders}
        else: 
            return { message: 'Cannot perform this operation' }, 401

    @authenticate
    def post(self, user_data):
        """Handles post requests to /parcels route"""
        message_dict = {}
        status_code = 200

        if user_data['is_admin']: 
            return {message: 'Cannot perform this operation'}, 401

        data = request.get_json()
        order = self.orders.add_order(data, user_data['user_id'])

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
        self.orders = Orders()

    @authenticate
    def get(self, id, user_data):
        message_dict = {}
        status_code = 200
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        order = self.orders.get_order(int_id)

        if order:
            return order
        else: 
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 400
        return message_dict, status_code
        
    @authenticate
    def put(self, id, user_data):
        message_dict = {}
        status_code = 200
        if not user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        if self.orders.is_order_there(int_id):
            self.orders.deliver_order(user_data['user id'], int_id)
            message_dict = {message: 'Status changed'} 
        else:       
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 400
        return message_dict, status_code            


class CancelOrder(Resource):
    """Handles the route /parcels/<parcel_id>/cancel"""

    def __init__(self):
        self.orders = Orders()

    @authenticate
    def put(self, id, user_data):
        message_dict = {}
        status_code = 200
        if user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        if self.orders.is_order_there(int_id):
            message_dict = {message: 'Order canceled'} 
        else:       
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 400
        return message_dict, status_code
