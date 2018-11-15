from itertools import count
from .mock_data import users
# Order statuses
canceled = 'Canceled'
delivered = 'Delivered'
in_transit = 'In-transit'
message = 'message'

orders = []
counter = count(start=100)

class ParcelOrders:
    """Orders Model"""
    def __init__(self):
        """Initialize parcel orders"""
        self.validator = Validator()

    def save(self, order, user_id):
        """Save data from POST request"""           
        message = self.validator.order_list_validator(order)

        if message == True:
            order['order_id'] = next(counter)
            order['curr_loc'] = order['pickup']
            order['status'] = in_transit
            order['user_id'] = user_id
            orders.append(order)
            return order
        else:
            return message

    def cancel_order(self, order_id):
        """Change order status to cancelled"""
        for order in orders:
            if order_id == order['order_id']:
                order['status'] = canceled
                return order
        return False

    def get_all_orders(self):
        """Returns all orders"""
        return orders

    def get_specific_order(self, order_id):
        """Returns specified order"""
        for order in orders:
            if order_id == order['order_id']:
                return order
        return False


    def get_all_user_orders(self, user_id):  # add tests
        """Returns all orders by specified user"""
        orders_list = []
        for order in orders:
            if order['user_id'] == user_id:
                orders_list.append(order)
        return orders_list

    def change_delivery_status(self, order_id):
        """Changed the specified order's delivery status"""
        for order in orders:
            if order_id == order['order_id']:
                order['status'] = delivered
                return order
        return False

    def get_order_owner(self, order_id):
        """Checks if user is in users"""
        isThere = False
        for order in orders:
            if order['order_id'] == order_id:
                return order['user_id']  # Returns key if user id
        return isThere


class Users:
    """Users operatons"""

    def __init__(self):
        """Initialize users class"""
        self.users = users

    def is_admin(self, user_id):
        """Returns the admin status of user"""
        for user in users:
            if user['user_id'] == user_id:
                return user['is_admin']

    def user_checker(self, user_email):
        """Checks if user is in users"""
        isThere = False
        for user in users:
            if user['email'] == user_email:
                return user['user_id']  # Returns key if user id is registered
        return isThere

    def password_checker(self, user_id, pswd):
        """Checks if password for specified user is valid"""
        for user in users:
            if user['user_id'] == user_id:
                return user['password'] == pswd

    



class Validator:
    """Validates incoming data"""

    def __init__(self):
        self.users = users

    def order_list_validator(self, order):
        """Check validity of parcels POST data"""
        keys = ['pickup', 'dest', 'recepient_name', 'recepient_no', 'weight']
        if not isinstance(order, dict):
            return {message: 'Payload must be a dictionary(object)'}
        if not len(order.keys()) == 5:
            return {message: 'Invalid number of order details'}
        if not sorted(list(order.keys())) == sorted(keys):
            return {message: 'One or more of object keys is invalid'}
        if not isinstance(order['weight'], int) and not isinstance(order['pickup'], int) and not isinstance(order['dest'], int) and not isinstance(order['recepient_name'], str) and not isinstance(order['recepient_no'], int):
            return {message: 'Wrong data type on one or more details'}
        if not len(str(order['recepient_no'])) == 9:
            return {message: 'Phone number must have ten digits'}
        if not len(str(order['pickup'])) == 8 and not len(str(order['dest'])) == 8:
            return {message: 'Addresses should be eight digits'}        
        return True

    