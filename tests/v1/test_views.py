import unittest
from run import app
import json
from app.api.v1.models import Validator, Users
from .mock_data import mock_data, message


class ParcelsTestCase(unittest.TestCase):
    """Parent Testcase class"""

    def setUp(self):
        """Sets up test variables"""
        self.app = app
        self.client = self.app.test_client(self)
        self.app.testing = True
        self.order = mock_data['order']
        data = json.dumps(mock_data['admin'])
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        self.admin_token_dict = json.loads(response.data)
        data = json.dumps(mock_data['user'])
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        self.user_token_dict = json.loads(response.data)
        self.client.post('api/v1/parcels', data=json.dumps(self.order), headers=self.user_token_dict, content_type="application/json")
        self.client.post('api/v1/parcels', data=json.dumps(self.order), headers=self.user_token_dict, content_type="application/json")


class GoodRequestTestCase(ParcelsTestCase):
    """This class tests views with valid requests"""

    def test_create_order(self):
        """Tests good requests to POST /parcels"""
        # Test with valid data format and right auth token
        response = self.client.post('/api/v1/parcels',
                                    data=json.dumps(self.order), content_type='application/json', headers=self.user_token_dict)
        self.assertTrue('order' in json.loads(response.data))
        self.assertEqual(json.loads(response.data)['message'], 'Order created')
        self.assertEqual(response.status_code, 201)

    def test_admin_change_order_status(self):
        """Tests PUT /parcels/<id>"""
        # Test with the right auth token
        response = self.client.put(
            'api/v1/parcels/100', headers=self.admin_token_dict)
        self.assertTrue('order' in json.loads(response.data))
        self.assertEqual(json.loads(response.data)['message'], 'Status changed')
        self.assertEqual(response.status_code, 200)

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        # Test with the right auth token
        self.client.post('api/v1/parcels', data=json.dumps(mock_data['order']), headers=self.user_token_dict)
        response = self.client.put(
            'api/v1/parcels/100/cancel', headers=self.user_token_dict)
        self.assertTrue('order' in json.loads(response.data))
        self.assertEqual(json.loads(response.data)['message'], 'Order canceled')
        self.assertEqual(response.status_code, 200)

    def test_get_all_orders(self):
        """Tests GET /parcels"""
        # Test with the right token
        response = self.client.get(
            'api/v1/parcels', headers=self.admin_token_dict)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue('orders' in data)

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        # Test with the right token
        response = self.client.get(
            'api/v1/users/102/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertTrue('orders' in data)
        self.assertEqual(response.status_code, 200)

    def test_get_specific_order(self):
        """Tests GET /parcels/<id>"""
        # Test with right auth token
        response = self.client.get(
            'api/v1/parcels/100', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('order' in data) 


class BadRequestTestCase(ParcelsTestCase):
    """This class tests views with invalid requests"""

    def test_create_order(self):
        """Tests bad requests to POST /parcels"""
        # Test with wrong data type
        response = self.client.post('/api/v1/parcels',
                                    data=json.dumps(['jay', 'bad', 'data']), content_type='application/json', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Payload must be a dictionary(object)'})
       
    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        # Test unregistered id
        # Correct format but not there
        response = self.client.put(
            'api/v1/parcels/35420/cancel', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {'message': 'No Parcel delivery order with that id'})
        # Test invalid format id
        response = self.client.put(
            'api/v1/parcels/35uh420/cancel', headers=self.user_token_dict)  # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

    def test_admin_change_order_status(self):
        """Tests bad requests to PUT /parcels/<id>"""
        # Test unregistered id
        # Correct format but not there
        response = self.client.put(
            'api/v1/parcels/35420', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {'message': 'No Parcel delivery order with that id'})
        # Test invalid format id
        response = self.client.put(
            'api/v1/parcels/35uh420', headers=self.admin_token_dict)  # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

    # def test_get_all_orders(self):
      #  """Tests bad requests to GET /parcels"""
       # pass

    def test_get_all_orders_by_user(self):
        """Tests bad requests to GET /users/<id>/parcels"""
        # Test with accessing other users parcels
        response = self.client.get(
            'api/v1/users/35530/parcels', headers=self.user_token_dict)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data), {
                         'message': 'Cannot perform this operation'})
        # Test with wrong format user id
        response = self.client.get(
            'api/v1/users/35fsv530/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})
        # Test with user with no orders
        response = self.client.get(
            'api/v1/users/104/parcels', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'No orders by that user'})
        self.assertEqual(response.status_code, 400)

    def test_get_specific_order(self):
        """Tests bad requests to GET /parcels/<id>"""
        # Test with wrong parcel id
        # Correct format but not there
        response = self.client.get(
            'api/v1/parcels/24034', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(
            data, {'message': 'No Parcel delivery order with that id'})
        self.assertEqual(response.status_code, 400)
        # Test with wrong parcel id format
        response = self.client.get(
            'api/v1/parcels/24034u', headers=self.user_token_dict)  # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Wrong id format'})
        self.assertEqual(response.status_code, 400)


class AuthGoodRequestTestCase(ParcelsTestCase):
    """Tests requests with valid authenticaton"""

    def test_login(self):
        """Tests good requests to POST /login"""
        # Admin login
        data = mock_data['admin']
        data = json.dumps(data)
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in data)
        # User login
        data = mock_data['user']
        data = json.dumps(data)
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in data)


class AuthBadRequestTestCase(ParcelsTestCase):
    """Tests with requests with invalid authentication"""

    def test_login(self):
        """Tests POST /login"""
        # Test login credentials
        response = self.client.post('api/v1/login')
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Email and password required'})
        self.assertEqual(response.status_code, 400)
        # Test bad datatype(not dict)
        response = self.client.post(
            'api/v1/login', data=json.dumps(['emm', 'jay']), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid data format'})
        self.assertEqual(response.status_code, 400)
        # Test bad email
        data = {'email': 'jb', 'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'User not registered'})
        self.assertEqual(response.status_code, 401)
        # Test bad password
        data = {'email': 'jratcher@gmail.com', 'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid password'})
        self.assertEqual(response.status_code, 401)
        # Test no email
        data = {'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Email not provided'})
        self.assertEqual(response.status_code, 400)
        # Test no password
        data = {'email': 'jratcher@gmail.com', }
        data = json.dumps(data)
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Password not provided'})
        self.assertEqual(response.status_code, 400)
        # Test with wrong format of login credentials
        data = ['Bad', 'data', 'format']
        data = json.dumps(data)
        response = self.client.post(
            'api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid data format'})
        self.assertEqual(response.status_code, 400)

    def test_create_parcel_authentication(self):
        """Tests POST requests to api/v1/parcels with no token, invalid token or unauthorized user"""
        # Test no token in headers
        response = self.client.post('api/v1/parcels', data=json.dumps(mock_data['order']))
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Token missing'})
        self.assertEqual(response.status_code, 401)
        # Test with admin token
        data = json.dumps(self.order)
        response = self.client.post('/api/v1/parcels',
                                    data=data, content_type='application/json', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)
        # Test with expired token
        data = json.dumps(self.order)
        response = self.client.post('/api/v1/parcels',
                                    data=data, content_type='application/json', headers={'token': mock_data['expired']})
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Token expired, login again'})
        self.assertEqual(response.status_code, 401)

    def test_get_all_orders_authentication(self):
        """Tests POST requests to api/v1/parcels with no token, invalid token or unauthorized user"""
        # Test with user token
        response = self.client.get(
            'api/v1/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)

    def test_specific_order_put_authentication(self):
        """Tests PUT requests to api/v1/parcels/<id> with no token, invalid token or unauthorized user"""
        # Test with user token
        response = self.client.put(
            'api/v1/parcels/100', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)
        # Test with invalid token
        response = self.client.put(
            'api/v1/parcels/100', headers={'token': 'jonjffriu8u483u8384u82'})
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid token'})
        self.assertEqual(response.status_code, 401)

    def test_cancel_order_authentication(self):
        """Tests PUT requests to api/v1/parcels/<parcel-id>/cancel with no token, invalid token or unauthorized user"""
        # Test with admin token
        response = self.client.put(
            'api/v1/parcels/100/cancel', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)


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
        #self.assertEqual(res_message, {message: 'Wrong data type on one or more details'})

    def test_user_checker(self):
        """Test user checker"""
        good_email = 'jratcher@gmail.com'
        bad_email = 'rigger@hotmail.com'
        # Test with email that is registered
        isThere = self.users.user_checker(good_email)
        self.assertEqual(isThere, 100)
        # Test with email thats not registered
        isThere = self.users.user_checker(bad_email)
        self.assertEqual(isThere, False)

    def test_password_checker(self):
        """Tests password checker"""
        password = 'ulembaya'
        bad_password = 'ngombe wewe'
        # Check with good password
        isValid = self.users.password_checker(100, password)
        self.assertEqual(isValid, True)
        # Check with bad password
        isValid = self.users.password_checker(100, bad_password)
        self.assertEqual(isValid, False)
