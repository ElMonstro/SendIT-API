import re
from validate_email import validate_email

message = 'message'


class Validator:
    """Validates incoming data"""

    def order_list_validator(self, order):
        """Check validity of parcels POST data"""
        keys = ['pickup', 'dest', 'recepient_name', 'recepient_no', 'weight']
        response = True
        while True:
            if not isinstance(order, dict):
                response = {message: 'Payload must be a dictionary(object)'}
                break
            if not len(order.keys()) == 5:
                response = {message: 'Invalid number of order details'}
                break
            if not sorted(list(order.keys())) == sorted(keys):
                resp_message = self.validate_order_keys(order)
                response = {message: "Unsuccessful, " + resp_message}
                break
            if self.validate_order_data(order):
                response = {message: "Unsuccessful, " +
                            self.validate_order_data(order)}
                break
            else:
                break
        return response

    def password_validator(self, password):
        """Validates password"""
        is_valid = True
        while True:
            if len(password) < 8:
                is_valid = 'Password must have eight characters'
                break
            if not re.search('[a-z]', password):
                is_valid = 'Password must have a lowercase character'
                break
            if not re.search('[A-Z]', password):
                is_valid = 'Password must have an uppercase character'
                break
            if not re.search('[0-9]', password):
                is_valid = 'Password must have a number'
                break
            if not re.search('[_@*#%!&$]', password):
                is_valid = 'Password must have one of this: _@*%!&$'
                break
            if re.search('\s', password):
                is_valid = "Password cannot have spaces"
                break
            else:
                break
        return is_valid

    def username_email_validator(self, username, email, user_dict):
        """Validates username and email"""
        response = True
        users_details = user_dict
        while True:
            if username in users_details['usernames']:
                response = "Username already taken"
                break
            elif email in users_details['emails']:
                response = "Email already used to register"
                break
            elif not validate_email(email):
                response = "Email invalid"
                break
            elif len(username) < 4:
                response = "Username cannot be less than four characters"
                break
            elif not re.search('^[A-Za-z]', username):
                response = "Username must start with a letter"
                break
            elif re.search('[@*#%!&$]', username):
                response = "Username cannot have this characters: @*#%!&$"
                break
            elif re.search('\s', username):
                response = "Username cannot have spaces"
                break
            else:
                break

        return response

    def status_validator(self, status):
        """Check is status is not in transit"""
        if status == 'Delivered':
            return 'Unsuccesful, order already delivered'
        if status == 'Canceled':
            return 'Unsuccessful, order is canceled'
        if status == 'Rejected':
            return 'Unsuccessful, order is rejected'
        return True

    def validate_order_data(self, order):
        """Validate data"""
        resp_message = None
        resp_list = []
        if not isinstance(order['weight'], int):
            resp_list.append("weight must be an integer")
        if not isinstance(order['recepient_no'], int):
            resp_list.append('recepient number must be an integer')
        if not isinstance(order['recepient_name'], str):
            resp_list.append('recepient name must be a string')
        if not isinstance(order['pickup'], str):
            resp_list.append('pickup location must be a string')
        if not isinstance(order['dest'], str):
            resp_list.append('destination location must be a string')
        if not order['pickup']:
            resp_list.append("pickup cannot be blank")
        if not order['dest']:
            resp_list.append("destination cannot be blank")
        if not len(str(order['recepient_no'])) == 9:
            resp_list.append('phone number must have nine digits')
        if len(str(order['recepient_name'])) < 3:
            resp_list.append('receipient name too short')
        if not str(order['recepient_name']).isalpha():
            resp_list.append('receipient name must be in letters')
        if resp_list:
            resp_message = ', '
            resp_message = resp_message.join(resp_list)
        return resp_message

    def validate_order_keys(self, order):
        """Ensures all keys are there"""
        resp_list = []
        resp_message = None
        try:
            order['dest']
        except KeyError:
            resp_list.append("the object must have a 'dest' key")
        try:
            order['pickup']
        except KeyError:
            resp_list.append("the object must have a 'pickup' key")
        try:
            order['weight']
        except KeyError:
            resp_list.append("the object must have a 'weight' key")
        try:
            order['recepient_name']
        except KeyError:
            resp_list.append(
                "the object must have a 'recepient_name' key")
        try:
            order['recepient_no']
        except KeyError:
            resp_list.append("the object must have a 'recepient_no' key")
        if resp_list:
            resp_message = ", "
            resp_message = resp_message.join(resp_list)
        return resp_message
