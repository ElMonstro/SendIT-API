import re
from validate_email import validate_email

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
            else: break
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
            else: break

        return response

            







#x = Validator().password_validator('Joshu@aE5mm')
#print(x)
    