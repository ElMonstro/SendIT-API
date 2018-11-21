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
            message_dict = {message: 'One order fetched', 'order': order}
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
        """Handles PUT parcels/<parcel_id>/cancel"""
        message_dict = {}
        status_code = 200
        if user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400
        
        status = self.orders.get_order_status(int_id)
            
        if status:
            if status == 'Delivered':
                return {message: 'Unsuccesful, order already delivered'}, 403
            if status == 'Canceled':
                return {message: 'Unsuccessful, order is canceled'}, 403 
            self.orders.cancel_order(int_id, user_data['user_id'])
            order_d = self.orders.get_order(int_id)
            message_dict = {message: 'Order canceled', 'order': order_d} 
        else:       
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 400
        return message_dict, status_code


class DeliverOrder(Resource):
    """Handle the route /parcels/<id>/deliver"""

    def __init__(self):
        self.orders = Orders()
        self.validators = Validator()

    @authenticate
    def put(self, id, user_data):
        """Handle put requests to route /parcels/<id>/deliver"""
        message_dict = {}
        status_code = 200
        if not user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        status = self.orders.get_order_status(int_id)

        if status:
            response = self.validators.status_validator(status)
            if response == True:
                self.orders.deliver_order(user_data['user_id'], int_id)
                order_d = self.orders.get_order(int_id)
                message_dict = {message: 'Status changed', 'order': order_d}
            else:
                return {message: response}, 403 
        else:       
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 400
        return message_dict, status_code            


class ChangeCurrentLocation(Resource):
    """Handles the route parcels/<parcel-id>/PresentLocation"""
    def __init__(self):
        self.orders = Orders()
        self.validators = Validator()

    @authenticate
    def put(self, id, user_data):
        """Handle request put requests to  parcels/<parcel-id>/PresentLocation"""
        message_dict = {}
        status_code = 200
        if not user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400
        
        data = request.get_json()
        try:
            curr_loc = data['curr_location']
        except KeyError:
            return {message: 'curr_location key not in object'}, 400
        except TypeError:
            return {message: 'Current Location must be an object'}, 400

        status = self.orders.get_order_status(int_id)

        if status:
            response = self.validators.status_validator(status)
            if response == True:
                self.orders.change_current_loc(user_data['user_id'],int_id, curr_loc)
                order_d = self.orders.get_order(int_id)
                message_dict = {message: 'Present location changed', 'order': order_d}
            else:
                return {message: response}, 403 
            
        else: 
            message_dict = {message: 'No parcel order with that id'}
            status_code = 400
        return message_dict, status_code


class ChangeDestLocation(Resource):
    """Handles the route parcels/<parcel-id>/PresentLocation"""
    def __init__(self):
        self.orders = Orders()
        self.validators = Validator()

    @authenticate
    def put(self, id, user_data):
        """Handle request put requests to  parcels/<parcel-id>/PresentLocation"""
        message_dict = {}
        status_code = 200
        if user_data['is_admin']:
            return { message: 'Cannot perform this operation' }, 401
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400
        
        data = request.get_json()
        try:
            dest_loc = data['dest_location']
        except KeyError:
            return {message: 'dest_location key not in object'}, 400
        except TypeError:
            return {message: 'Destination Location must be an object'}, 400

        str(dest_loc)

        status = self.orders.get_order_status(int_id)

        if status:
            response = self.validators.status_validator(status)
            if response == True:
                self.orders.change_dest_loc(user_data['user_id'],int_id, dest_loc)
                order_d = self.orders.get_order(int_id)
                message_dict = {message: 'Destination location changed', 'order': order_d}
            else:
                return {message: response}, 403 
            
        else: 
            message_dict = {message: 'No parcel order with that id'}
            status_code = 400
        return message_dict, status_code

        
        
        

