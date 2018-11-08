
# Order statuses
canceled = 'Canceled'
delivered = 'Delivered'
in_transit = 'In-transit'
# Admin statuses
admin = True
not_admin = False

# Dummy orders
orders = {
   #id   userid  pickup addr  dest address kg  status
    321: [532, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    453: [352, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    133: [254, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    301: [686, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    353: [103, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    633: [345, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    365: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    495: [675, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    127: [109, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    249: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    132: [619, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    808: [805, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    809: [532, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    810: [352, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    811: [254, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    812: [686, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    813: [103, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    814: [345, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    815: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    816: [675, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    817: [109, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    818: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    819: [619, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    820: [805, '5 6535 453', '8 5465 742', 6, 'Canceled']
}

users = {
 # userid  email                 password   isadmin
    100: ['jratcher@gmail.com', 'ulembaya', admin],
    102: ['dan@gmail.com', 'ulembaya', not_admin],
    103: ['abby@gmail.com', 'ulembaya', not_admin],
    104: ['totodi@gmail.com', 'ulembaya', not_admin],
    105: ['milly@gmail.com', 'ulembaya', not_admin],
    350: ['callen@gmail.com', 'ulembaya', not_admin], 
}

class ParcelOrders:
    """Orders Model"""
    def __init__(self):
        self.orders = orders
        self.order_no = 100

    def save(self, order):
        """Save data from POST request"""
        validator = Validator()        
        try:
            order_list = order['order']
        except TypeError:
            return False
        
        valid = validator.order_list_validator(order_list)

        if valid:
            orders[self.order_no] = order_list
            self.order_no = self.order_no + 1
            return True
        else:
            return False

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

    def get_all_user_orders(self, user_id):
        """Returns all orders by specified user"""
        order_list = {}
        for key, value in self.orders.items():
            if user_id == value[0]:
                order_list[key] = value
        if not  order_list:
            return False
        return {'orders': order_list}

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
                return key # Returns key if user id is registered               
        return isThere

    def password_checker(self,user_id, pswd):
        """Checks if password for specified user is valid"""
        if self.users[user_id][1] == pswd:
            return True
        return False
        
