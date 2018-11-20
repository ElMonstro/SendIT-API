import unittest
from run import app
import json
from app.api.v2.models.user_models import Users
from .mock_data import mock_data, message
from app.api.v2.utils.validators import Validator

class ValidatorsTestCase(unittest.TestCase):
    """Tests edge cases"""

    def setUp(self):
        """Set up test variables"""
        self.validator = Validator()
        self.users = Users()

    def test_order_post_data_validator(self):
        """Tests order_list_validator"""
        order_list_validator = self.validator.order_list_validator
        good_data = mock_data['order']
       
        # Test with good data
        valid = order_list_validator(good_data)
        self.assertEqual(valid, True)
        message = 'message'
        # Test with bad data
        res_message = order_list_validator(mock_data['bad_key'])
        self.assertEqual(res_message, {message: 'One or more of object keys is invalid'})
        res_message = order_list_validator(mock_data['invalid_addr'])
        self.assertEqual(res_message, {message: 'Addresses should be eight digits'}  )
        res_message = order_list_validator(mock_data['less'])
        self.assertEqual(res_message, {message: 'Invalid number of order details'} )
        res_message = order_list_validator(mock_data['invalid_tel'])
        self.assertEqual(res_message, {message: 'Phone number must have ten digits'} )
        res_message = order_list_validator(mock_data['invalid_data'])
        self.assertEqual(res_message, {message: 'Wrong data type on one or more details'})
        res_message = order_list_validator(mock_data['bad_name'])
        self.assertEqual(res_message, {message: 'Receipient name too short'})
        # Add test

    def test_password_validator(self):
        """Test the password validator"""
        # Test with bad passwords
        pass_validator = self.validator.password_validator 
        pass_list = mock_data['bad_pass']
        is_valid = pass_validator(pass_list[0])
        self.assertEqual(is_valid, 'Password must have eight characters')
        is_valid = pass_validator(pass_list[1])
        self.assertEqual(is_valid, 'Password must have a lowercase character')
        is_valid = pass_validator(pass_list[2])
        self.assertEqual(is_valid, 'Password must have an uppercase character')
        is_valid = pass_validator(pass_list[3])
        self.assertEqual(is_valid, 'Password must have a number')
        is_valid = pass_validator(pass_list[4])
        self.assertEqual(is_valid, 'Password must have one of this: _@*%!&$')
        is_valid = pass_validator(pass_list[5])
        self.assertEqual(is_valid, 'Password cannot have spaces')
        # Test with good password
        is_valid = pass_validator(mock_data['good_pass'])
        self.assertEqual(is_valid, True)


    def test_email_username_validator(self):
        """Test the email and username validator"""
        # Test with good data
        validator = self.validator.username_email_validator
        resp = validator('moracha', 'moracha@gmail.com', mock_data['user_dets'])
        self.assertTrue(resp)
        # Test with bad data
        # Registered username
        validator = self.validator.username_email_validator
        resp = validator(mock_data['reg_usernm'], 'moracha@gmail.com', mock_data['user_dets'])
        self.assertEqual(resp, "Username already taken")
        # Registered email
        validator = self.validator.username_email_validator
        resp = validator('moracha', mock_data['reg_email'], mock_data['user_dets'])
        self.assertEqual(resp, "Email already used to register")
        # invalid email
        validator = self.validator.username_email_validator
        resp = validator('moracha', mock_data['bad_email'], mock_data['user_dets'])
        self.assertEqual(resp, "Email invalid")
        # username less than four characters
        validator = self.validator.username_email_validator
        resp = validator('moa', 'josh@gmail.com', mock_data['user_dets'])
        self.assertEqual(resp, "Username cannot be less than four characters")
        # username with characters
        validator = self.validator.username_email_validator
        resp = validator(mock_data['space_usnm'], 'josh@gmail.com', mock_data['user_dets'])
        self.assertEqual(resp, "Username cannot have spaces")

    def test_status_validator(self):
        """Test if status is delivered"""
        validator = self.validator.status_validator
        response = validator('Delivered')
        self.assertEqual(response, 'Unsuccesful, order already delivered')
        response = validator('Canceled')
        self.assertEqual(response, 'Unsuccessful, order is canceled')
        response = validator('In-transit')
        self.assertTrue(response)


        



        

