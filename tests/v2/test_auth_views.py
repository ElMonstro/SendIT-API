import unittest
from run import app
import json
from app.api.v2.models.user_models import Users
from .mock_data import mock_data, message
from .test_orders_views import ParcelsTestCase
from app.api.v2.utils.validators import Validator
from app.db_config import DbConnect


class AuthGoodRequestTestCase(ParcelsTestCase):
    """Tests requests with valid authenticaton"""

    def test_login(self):
        """Tests good requests to POST auth/login"""
        # Admin login
        data = mock_data['admin']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in data)
        # User login
        data = mock_data['user']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in data)
        self.assertEqual(data['message'], 'Login successful')

class TestRegister(ParcelsTestCase):
    """Test valid request to /auth/sighnup"""

    def test_register(self):
        """Tests good requests to POST auth/register"""
        # Register good data
        data = mock_data['register']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/signup', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User registered')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in data)

    def tearDown(self):
        """Delete user records"""
        self.db_conn.delete_latest_user()


class AuthBadRequestTestCase(ParcelsTestCase):
    """Tests with requests with invalid authentication"""

    def test_login(self):
        """Tests POST /login"""
        # Test login credentials
        response = self.client.post('api/v2/auth/login')
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Username and password required'})
        self.assertEqual(response.status_code, 400)
        # Test bad datatype(not dict)
        response = self.client.post(
            'api/v2/auth/login', data=json.dumps(['emm', 'jay']), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid data format'})
        self.assertEqual(response.status_code, 400)
        # Test bad username
        data = {'username': 'jb', 'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'User not registered'})
        self.assertEqual(response.status_code, 401)
        # Test bad password
        data = {'username': 'admin', 'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid password'})
        self.assertEqual(response.status_code, 401)
        # Test no username
        data = {'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Username not provided'})
        self.assertEqual(response.status_code, 400)
        # Test no password
        data = {'username': 'admin', }
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Password not provided'})
        self.assertEqual(response.status_code, 400)
        # Test with wrong format of auth/login credentials
        data = ['Bad', 'data', 'format']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid data format'})
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        """Test bad request to route /auth/signup"""
        # Test no username
        data = {'password': 'pwd', 'email': 'Josh'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/signup', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Username not provided'})
        self.assertEqual(response.status_code, 400)
        # Test no password
        data = {'username': 'admin', 'email': 'a@g.com'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/signup', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Password not provided'})
        self.assertEqual(response.status_code, 400)
        # Test no email
        data = {'username': 'admin', 'password': 'a@g.com'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/signup', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Email not provided'})
        self.assertEqual(response.status_code, 400)
        # Test with wrong format of auth/login credentials
        data = ['Bad', 'data', 'format']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/signup', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid data format'})
        self.assertEqual(response.status_code, 400)
        # Register bad email
        data = mock_data['bad_email_r']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/signup', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Email invalid')
        self.assertEqual(response.status_code, 400)
        # Test bad usernsmr
        data = mock_data['bad_usern_r']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/auth/signup', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Username cannot be less than four characters")
        self.assertEqual(response.status_code, 400)

    def test_create_parcel_authentication(self):
        """Tests POST requests to api/v2/parcels with no token, invalid token or unauthorized user"""
        # Test no token in headers
        response = self.client.post(
            'api/v2/parcels', data=json.dumps(mock_data['order']))
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Token missing'})
        self.assertEqual(response.status_code, 401)
        # Test with admin token
        data = json.dumps(self.order)
        response = self.client.post('/api/v2/parcels',
                                    data=data, content_type='application/json', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(
            data, {'message': 'You are not authorized to perform this operation'})
        self.assertEqual(response.status_code, 403)
        # Test with expired token
        data = json.dumps(self.order)
        response = self.client.post('/api/v2/parcels',
                                    data=data, content_type='application/json', headers={'token': mock_data['expired']})
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Token expired, login again'})
        self.assertEqual(response.status_code, 401)

    def test_get_all_orders_authentication(self):
        """Tests POST requests to api/v2/parcels with no token, invalid token or unauthorized user"""
        # Test with user token
        response = self.client.get(
            'api/v2/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(
            data, {message: 'You are not authorized to perform this operation'})
        self.assertEqual(response.status_code, 403)

    def test_deliver_authentication(self):
        """Tests PUT requests to api/v2/parcels/<id> with no token, invalid token or unauthorized user"""
        # Test with user token
        response = self.client.put(
            'api/v2/parcels/100/deliver', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(
            data, {message: 'You are not authorized to perform this operation'})
        self.assertEqual(response.status_code, 403)
        # Test with invalid token
        response = self.client.put(
            'api/v2/parcels/100/deliver', headers={'token': 'jonjffriu8u483u8384u82'})
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid token'})
        self.assertEqual(response.status_code, 401)

    def test_cancel_order_authentication(self):
        """Tests PUT requests to api/v2/parcels/<parcel-id>/cancel with no token, invalid token or unauthorized user"""
        # Test with admin token
        response = self.client.put(
            'api/v2/parcels/100/cancel', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(
            data, {message: 'You are not authorized to perform this operation'})
        self.assertEqual(response.status_code, 403)
