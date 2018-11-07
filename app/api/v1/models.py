
# Order statuses
canceled = 'Canceled'
delivered = 'Delivered'

# Dummy orders
orders = {
   #id   userid  pickup addr  dest address kg  status
    321: [532, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    453: [352, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    133: [254, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    301: [686, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    353: [350, '4 5435 324', '6 5356 353', 3, 'Delivered'],
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
    813: [350, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    814: [345, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    815: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    816: [675, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    817: [109, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    818: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    819: [619, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    820: [805, '5 6535 453', '8 5465 742', 6, 'Canceled']
}

class ParcelOrders:
    """Orders Model"""
    def __init__(self):
        self.orders = orders
        self.order_no = 100

    def save(self, order_list):
        """Save data from POST request"""
        orders[self.order_no] = order_list
        self.order_no = self.order_no + 1
        return True

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





