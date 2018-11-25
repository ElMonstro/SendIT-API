from flask import request
from flask_restful import Resource
from app.api.v2.models.order_models import Orders
import jwt
import datetime
from instance.config import DevelopmentConfig
from functools import wraps
from app.api.v2.utils.auth_decorator import authenticate
from app.api.v2.utils.validators import Validator

message = 'message'
canceled = "Canceled"
rejected = "Rejected"
delivered = "Delivered"
in_transit = "In-transit"
current_location = "current_location"
dest = "dest"


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
            return {message: 'You are not authorized to perform this operation'}, 403

    @authenticate
    def post(self, user_data):
        """Handles post requests to /parcels route"""
        message_dict = {}
        status_code = 200

        if user_data['is_admin']:
            return {message: 'You are not authorized to perform this operation'}, 403

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
            status_code = 404
        return message_dict, status_code


class CancelOrder(Resource):
    """Handles the route /parcels/<parcel_id>/cancel"""

    def __init__(self):
        self.orders = Orders()
        self.validators = Validator()

    @authenticate
    def put(self, id, user_data):
        """Handles PUT parcels/<parcel_id>/cancel"""
        message_dict = {}
        status_code = 200
        if user_data['is_admin']:
            return {message: 'You are not authorized to perform this operation'}, 403
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        order = self.orders.get_order(int_id)

        if order:
            if not order['user_id'] == user_data['user_id']:
                return {message: 'You are not authorized to perform this operation'}, 403
            status = order['status']
            error_message = self.validators.status_validator(status)
            if error_message == True:
                self.orders.change_order_status(
                    user_id=user_data['user_id'], order_id=int_id, status=canceled)
                order_d = self.orders.get_order(int_id)
                message_dict = {message: 'Order canceled', 'order': order_d}
            else:
                return {message: error_message}, 400
        else:
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 404
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
            return {message: 'You are not authorized to perform this operation'}, 403
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        order = self.orders.get_order(int_id)

        if order:
            status = order['status']
            error_message = self.validators.status_validator(status)
            if error_message == True:
                self.orders.change_order_status(
                    order_id=int_id, status=delivered)
                order_d = self.orders.get_order(int_id)
                message_dict = {message: 'Order delivered', 'order': order_d}
            else:
                return {message: error_message}, 400
        else:
            message_dict = {message: 'No Parcel delivery order with that id'}
            status_code = 404
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
            return {message: 'You are not authorized to perform this operation'}, 403
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
            return {message: 'Current Location must be in an object'}, 400

        order = self.orders.get_order(int_id)

        if order:
            status = order['status']
            response = self.validators.status_validator(status)
            if response == True:
                self.orders.change_location(
                    order_id=int_id, location=curr_loc, column=current_location)
                order_d = self.orders.get_order(int_id)
                message_dict = {
                    message: 'Present location changed', 'order': order_d}
            else:
                return {message: response}, 400

        else:
            message_dict = {message: 'No parcel order with that id'}
            status_code = 404
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
            return {message: 'You are not authorized to perform this operation'}, 403
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
            return {message: 'Destination Location must be in an object'}, 400

        order = self.orders.get_order(int_id)

        if order:
            status = order['status']
            response = self.validators.status_validator(status)
            if response == True:
                self.orders.change_location(
                    order_id=int_id, location=dest_loc, column=dest)
                order_d = self.orders.get_order(int_id)
                message_dict = {
                    message: 'Destination location changed', 'order': order_d}
            else:
                return {message: response}, 400

        else:
            message_dict = {message: 'No parcel order with that id'}
            status_code = 404
        return message_dict, status_code
