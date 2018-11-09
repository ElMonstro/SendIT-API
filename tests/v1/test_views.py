import unittest
from run import app
import json
from app.api.v1.models import Validator


order = {'order': ['532', '4 5345 343', '4 5343 343', 5, 'In-transit']}
response_data = {"order": { "321": [532, "4 5345 343", "4 5343 343", 5, "Canceled"]}}

users_orders = {
    "orders": {
        "353": [103, "4 5435 324", "6 5356 353", 3, "Delivered" ],
        "813": [103, "4 5435 324", "6 5356 353", 3,  "Delivered"]
    }
}

# Login credentials
admin_login = {'email': 'jratcher@gmail.com',
                    'password': 'ulembaya'}

user_login = {'email': 'abby@gmail.com',
                    'password': 'ulembaya'}

message = 'message'

expired_token =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIGlkIjoxMDMsImVtYWlsIjoiYWJieUBnbWFpbC5jb20iLCJpc19hZG1pbiI6ZmFsc2UsImV4cCI6MTU0MTc0MTE0MX0.uckKmwZ3YqQU4M36xhbEcXLx4KQ4B4Ej-Vua4Yw0HCM"



class ParcelsTestCase(unittest.TestCase):
    """Parent Testcase class"""

    def setUp(self):
        """Sets up test variables"""
        self.app = app
        self.client = self.app.test_client(self)
        self.app.testing = True
        self.order = order
        data = json.dumps(admin_login)
        response = self.client.post('api/v1/login', content_type="application/json", data=data)
        self.admin_token_dict = json.loads(response.data)      
        data = json.dumps(user_login)
        response = self.client.post('api/v1/login', content_type="application/json", data=data)
        self.user_token_dict = json.loads(response.data)
        
        
        
class GoodRequestTestCase(ParcelsTestCase):
    """This class tests views with valid requests"""

    def test_create_order(self):
        """Tests good requests to POST /parcels"""
        # Test with valid data format and right auth token
        response = self.client.post('/api/v1/parcels',
                    data=json.dumps(self.order), content_type='application/json', headers=self.user_token_dict )        
        self.assertEqual(json.loads(response.data), {'message': 'Order created'} )
        self.assertEqual(response.status_code, 201)


    def test_admin_change_order_status(self):
        """Tests PUT /parcels/<id>"""
        # Test with the right auth token
        response = self.client.put('api/v1/parcels/321', headers=self.admin_token_dict)
        self.assertEqual(json.loads(response.data), {message: 'Status changed'})
        self.assertEqual(response.status_code, 200)

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        # Test with the right auth token
        response = self.client.put('api/v1/parcels/321/cancel', headers=self.user_token_dict)
        self.assertEqual(json.loads(response.data), {message: 'Order canceled'})
        self.assertEqual(response.status_code, 200)


    def test_get_all_orders(self):
        """Tests GET /parcels"""
        # Test with the right token
        response = self.client.get('api/v1/parcels', headers=self.admin_token_dict)
        self.assertEqual(response.status_code, 200)
        

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        # Test with the right token 
        response = self.client.get('api/v1/users/103/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)        
        self.assertEqual(data, users_orders)

    def test_get_specific_order(self):
        """Tests GET /parcels/<id>"""
        # Test with right auth token
        response = self.client.get('api/v1/parcels/321', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, response_data)


class BadRequestTestCase(ParcelsTestCase):
    """This class tests views with invalid requests"""

    def test_create_order(self):
        """Tests bad requests to POST /parcels"""
        # Test with wrong data format
        response = self.client.post('/api/v1/parcels',
                    data=json.dumps(['jay', 'bad', 'data']), content_type='application/json', headers=self.user_token_dict )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {message: 'Invalid data format'})

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        # Test unregistered id 
        response = self.client.put('api/v1/parcels/35420/cancel', headers=self.user_token_dict) # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)        
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})
        # Test invalid format id
        response = self.client.put('api/v1/parcels/35uh420/cancel', headers=self.user_token_dict) # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

    def test_admin_change_order_status(self):
        """Tests bad requests to PUT /parcels/<id>"""
        # Test unregistered id
        response = self.client.put('api/v1/parcels/35420', headers=self.admin_token_dict) # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)        
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})
        # Test invalid format id
        response = self.client.put('api/v1/parcels/35uh420', headers=self.admin_token_dict) # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

        

    # def test_get_all_orders(self):
      #  """Tests bad requests to GET /parcels"""
       # pass

    def test_get_all_orders_by_user(self):
        """Tests bad requests to GET /users/<id>/parcels"""
        # Test with accessing other users parcels  
        response = self.client.get('api/v1/users/35530/parcels', headers=self.user_token_dict)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data), {'message': 'Cannot perform this operation'})
        # Test with wrong format user id
        response = self.client.get('api/v1/users/35fsv530/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})


    def test_get_specific_order(self):
        """Tests bad requests to GET /parcels/<id>"""
        # Test with wrong parcel id
        response = self.client.get('api/v1/parcels/24034', headers=self.user_token_dict)  # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})
        self.assertEqual(response.status_code, 400)
        # Test with wrong parcel id format
        response = self.client.get('api/v1/parcels/24034u', headers=self.user_token_dict) # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Wrong id format'})
        self.assertEqual(response.status_code, 400)    


class AuthGoodRequestTestCase(ParcelsTestCase):
    """Tests requests with valid authenticaton"""

    def test_login(self):
        """Tests good requests to POST /login"""
        # Admin login
        data = admin_login
        data = json.dumps(data)
        response = self.client.post('api/v1/login', content_type="application/json", data=data)
        #data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        # User login
        data = user_login
        data = json.dumps(data)
        response = self.client.post('api/v1/login', content_type="application/json", data=data)
       # data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    


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
        response = self.client.post('api/v1/login', data=json.dumps(['emm', 'jay']), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid data format'})
        self.assertEqual(response.status_code, 400)
        # Test bad email
        data = {'email': 'jb', 'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post('api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'User email not found'})
        self.assertEqual(response.status_code, 401)
        # Test bad password
        data = {'email': 'jratcher@gmail.com', 'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post('api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid password'})
        self.assertEqual(response.status_code, 401)
        # Test no email
        data = {'password': 'pwd'}
        data = json.dumps(data)
        response = self.client.post('api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Email not provided'})
        self.assertEqual(response.status_code, 400)
        # Test no password
        data = {'email': 'jratcher@gmail.com',}
        data = json.dumps(data)
        response = self.client.post('api/v1/login', content_type="application/json", data=data)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Password not provided'})
        self.assertEqual(response.status_code, 400)

    def test_create_parcel_authentication(self):
        """Tests POST requests to api/v1/parcels with no token, invalid token or unauthorized user"""
        # Test no token in headers
        response = self.client.post('api/v1/parcels', data=json.dumps(order))
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Token missing'})
        self.assertEqual(response.status_code, 401)
        # Test with admin token
        data = json.dumps(self.order)
        response = self.client.post('/api/v1/parcels',
                    data=data, content_type='application/json', headers=self.admin_token_dict )   
        data = json.loads(response.data)     
        self.assertEqual(data, {'message': 'Cannot perform this operation'} )
        self.assertEqual(response.status_code, 401)
        # Test with expired token
        data = json.dumps(self.order)
        response = self.client.post('/api/v1/parcels',
                    data=data, content_type='application/json', headers={'token': expired_token} )   
        data = json.loads(response.data)     
        self.assertEqual(data, {'message': 'Token expired, login again'} )
        self.assertEqual(response.status_code, 401)


    def test_get_all_orders_authentication(self):
        """Tests POST requests to api/v1/parcels with no token, invalid token or unauthorized user"""
        # Test with user token
        response = self.client.get('api/v1/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)

    def test_specific_order_put_authentication(self):
        """Tests PUT requests to api/v1/parcels/<id> with no token, invalid token or unauthorized user"""
        # Test with user token
        response = self.client.put('api/v1/parcels/321', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)
        # Test with invalid token
        response = self.client.put('api/v1/parcels/321', headers={'token': 'jonjffriu8u483u8384u82'})
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Invalid token'})
        self.assertEqual(response.status_code, 401)

    def test_cancel_order_authentication(self):
        """Tests PUT requests to api/v1/parcels/<parcel-id>/cancel with no token, invalid token or unauthorized user"""
        # Test with admin token
        response = self.client.put('api/v1/parcels/321/cancel', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {message: 'Cannot perform this operation'})
        self.assertEqual(response.status_code, 401)


        

        







class ValidatorsTestCase(unittest.TestCase):
    """Tests edge cases"""

    def setUp(self):
        """Set up test variables"""
        self.validator = Validator()

    def test_order_post_data_validator(self):
        """Tests order_list_validator"""
        order_list_validator = self.validator.order_list_validator
        good_data = [532, '4 5345 343', '4 5343 343', 5, 'In-transit']
        bad_data = [ 'String', ['string', 42453, 53245, 'String', 42524],
         ['string', 42453, 53245, 'String', 'fsags'],
         ['string', 53245, 'String', 42524],  43,
         {'order': ['string', 42453, 53245, 'String', 42524]}
         ]    
        # Test with good data
        valid = order_list_validator(good_data)
        self.assertEqual(valid, True)
        # Test with bad data
        for data in bad_data:
            valid = order_list_validator(data)
            self.assertEqual(valid, False)

    def test_user_checker(self):
        """Test user checker"""
        good_email = 'jratcher@gmail.com'
        bad_email = 'rigger@hotmail.com'
        # Test with email that is registered
        isThere = self.validator.user_checker(good_email)
        self.assertEqual(isThere, 100)
        # Test with email thats not registered
        isThere = self.validator.user_checker(bad_email)
        self.assertEqual(isThere, False) 

    def test_password_checker(self):
        """Tests password checker"""
        password = 'ulembaya'
        bad_password = 'ngombe wewe'
        # Check with good password
        isValid = self.validator.password_checker(100, password)
        self.assertEqual(isValid, True)
        # Check with bad password
        isValid = self.validator.password_checker(100, bad_password)
        self.assertEqual(isValid, False) 

        
        


    




        

