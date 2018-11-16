message = 'message'

class Validator:
    """Validates incoming data"""

    def order_list_validator(self, order):
        """Check validity of parcels POST data"""
        keys = ['pickup', 'dest', 'recepient_name', 'recepient_no', 'weight']
        if not isinstance(order, dict):
            return {message: 'Payload must be a dictionary(object)'}
        if not len(order.keys()) == 5:
            return {message: 'Invalid number of order details'}
        if not sorted(list(order.keys())) == sorted(keys):
            return {message: 'One or more of object keys is invalid'}
        if not isinstance(order['weight'], int) or not isinstance(order['pickup'], int) or not isinstance(order['dest'], int) or not isinstance(order['recepient_name'], str) or not isinstance(order['recepient_no'], int):
            return {message: 'Wrong data type on one or more details'}
        if not len(str(order['recepient_no'])) == 9:
            return {message: 'Phone number must have ten digits'}
        if not len(str(order['pickup'])) == 8 and not len(str(order['dest'])) == 8:
            return {message: 'Addresses should be eight digits'}
        if len(order['recepient_name']) < 3:
            return {message: 'Receipient name too short'}
        if not order['recepient_name'].isalpha():
            return {message: 'Receipient name must be in letters'}        
        return True