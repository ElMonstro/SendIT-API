from flask import request
from flask_restful  import Resource
import datetime
from instance.config import DevelopmentConfig
from app.api.v2.models.order_models import Orders
from app.api.v2.models.user_models import Users
from app.api.v2.utils.auth_decorator import authenticate


message = 'message'

class UserParcels(Resource):
    """Handles the route /users/<user_id>/parcels"""
    
    def __init__(self):
        self.orders = Orders()

    @authenticate
    def get(self, id, user_data):  
        message_dict = { message: 'You are not authorized to perform this operation' }
        status_code = 403
        try:
            int_id = int(id)
        except ValueError:
            return {message: 'Wrong id format'}, 400

        if user_data['user_id'] == int(id) or user_data['is_admin']:
            orders = self.orders.get_users_orders(int_id)
            if not orders:
                return {message: 'No orders by that user'}, 404
            return {message: 'All user orders', 'orders': orders}  
        # If user not admin or his/her id is not equal to the user id are  trying to access
        return message_dict, status_code