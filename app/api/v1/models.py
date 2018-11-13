from .mock_data import users, orders, admin, delivered, in_transit, canceled, not_admin


class ParcelOrders:
    """Orders Model"""

    def __init__(self):
        self.orders = orders
        self.order_no = 100

    def save(self, order):
        """Save data from POST request"""
        validator = Validator()
        is_successful = True
        try:
            order_list = order['order']
        except TypeError:
            return False

        valid = validator.order_list_validator(order_list)

        if valid:
            orders[self.order_no] = order_list
            self.order_no = self.order_no + 1
            is_successful = True
        else:
            is_successful = False
        return is_successful

    def cancel_order(self, order_id):
        """Change order status to cancelled"""
        if order_id in self.orders.keys():
            self.orders[order_id][4] = canceled
            return True
        else:
            return False

    def get_all_orders(self):
        """Returns all orders"""
        return self.orders

    def get_specific_order(self, order_id):
        """Returns specified order"""
        if order_id in self.orders.keys():
            return {'order': {str(order_id): orders[order_id]}}
        else:
            return False

    def get_all_user_orders(self, user_id):  # add tests
        """Returns all orders by specified user"""
        order_list = {}
        for key, value in self.orders.items():
            if user_id == value[0]:
                order_list[key] = value
        if order_list:
            return {'orders': order_list}
        else:
            return False

    def change_delivery_status(self, order_id):
        """Changed the specified order's delivery status"""
        if order_id in self.orders.keys():
            orders[order_id][4] = delivered
            return True
        else:
            return False


class Users:
    """Users operatons"""

    def __init__(self):
        self.users = users

    def is_admin(self, user_id):
        """Returns the admin status of user"""
        return self.users[user_id][2]


class Validator:
    """Validates incoming data"""

    def __init__(self):
        self.users = users

    def order_list_validator(self, order_list):
        """Check validity of parcels POST data"""
        if not isinstance(order_list, list):
            return False
        if not len(order_list) == 5:
            return False
        if not isinstance(order_list[0], int) and not isinstance(order_list[1], str) and not isinstance(order_list[2], str) and not isinstance(order_list[3], int) and not isinstance(order_list[4], str):
            return False
        if not order_list[4] in [delivered, in_transit, canceled]:
            return False
        return True

    def user_checker(self, user_email):
        """Checks if user is in users"""
        isThere = False
        for key, value in users.items():
            if value[0] == user_email:
                return key  # Returns key if user id is registered
        return isThere

    def password_checker(self, user_id, pswd):
        """Checks if password for specified user is valid"""
        if self.users[user_id][1] == pswd:
            return True
        return False