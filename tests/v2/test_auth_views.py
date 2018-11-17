import unittest
from run import app
import json
from app.api.v2.models.user_models import Users
from .mock_data import mock_data, message
from .test_orders_views import ParcelsTestCase
from app.api.v2.utils.validators import Validator

class AuthGoodRequestTestCase(ParcelsTestCase):
    """Tests requests with valid authenticaton"""

    def test_login(self):
        """Tests good requests to POST /login"""
        # Admin login
        data = mock_data['admin']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in data)
        # User login
        data = mock_data['user']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in data)


class AuthBadRequestTestCase(ParcelsTestCase):
    """Tests with requests with invalid authentication"""

    def test_login(self):
        """Tests POST /login"""
        # Test login credentials
        response = self.client.post('api/v2/login')
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Email and password required'})
        self.assertEqual(response.status_code, 400)
        # Test bad datatype(not dict)
        response = self.client.post(
            'api/v2/login', data=json.dumps(['emm', 'jay']), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid data format'})
        self.assertEqual(response.status_code, 400)
        # Test bad email
        data = {'email': 'jb', 'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'User not registered'})
        self.assertEqual(response.status_code, 401)
        # Test bad password
        data = {'email': 'jratcher@gmail.com', 'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid password'})
        self.assertEqual(response.status_code, 401)
        # Test no email
        data = {'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Email not provided'})
        self.assertEqual(response.status_code, 400)
        # Test no password
        data = {'email': 'jratcher@gmail.com', }
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Password not provided'})
        self.assertEqual(response.status_code, 400)
        # Test with wrong format of login credentials
        data = ['Bad', 'data', 'format']
        data = json.dumps(data)
        response = self.client.post(
            'api/v2/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid data format'})
        self.assertEqual(response.status_code, 400)

    def test_create_parcel_authentication(self):
        """Tests POST requests to api/v2/parcels with no token, invalid token or unauthorized user"""
        # Test no token in headers
        response = self.client.post('api/v2/parcels', data=json.dumps(mock_data['order']))
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Token missing'})
        self.assertEqual(response.status_code, 401)
        # Test with admin token
        data = json.dumps(self.order)
        response = self.client.post('/api/v2/parcels',
                                    data=data, content_type='application/json', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)
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
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)

    def test_specific_order_put_authentication(self):
        """Tests PUT requests to api/v2/parcels/<id> with no token, invalid token or unauthorized user"""
        # Test with user token
        response = self.client.put(
            'api/v2/parcels/100', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)
        # Test with invalid token
        response = self.client.put(
            'api/v2/parcels/100', headers={'token': 'jonjffriu8u483u8384u82'})
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid token'})
        self.assertEqual(response.status_code, 401)

    def test_cancel_order_authentication(self):
        """Tests PUT requests to api/v2/parcels/<parcel-id>/cancel with no token, invalid token or unauthorized user"""
        # Test with admin token
        response = self.client.put(
            'api/v2/parcels/100/cancel', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)


