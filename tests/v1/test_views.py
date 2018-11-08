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

user_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIGlkIjoxMDMsImVtYWlsIjoiYWJieUBnbWFpbC5jb20iLCJpc19hZG1pbiI6ZmFsc2UsImV4cCI6MTU0MjI0NDM4NH0.wLLCb3qYi8ET1NgRj7oH9d9dhxN8hsJp3U81Rmjk4lA"
admin_token =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIGlkIjoxMDAsImVtYWlsIjoianJhdGNoZXJAZ21haWwuY29tIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTU0MjI0NDQ4M30.q_JxTQ3FmDPMe01kIg8-aEJ4Tiik_J2FU39NjiLsazU"



class ParcelsTestCase(unittest.TestCase):
    """Parent Testcase class"""

    def setUp(self):
        """Sets up test variables"""
        self.app = app
        self.client = self.app.test_client(self)
        self.app.testing = True
        self.order = order
        admin_data = json.dumps({'email': 'jratcher@gmail.com',
                                  'password': 'ulembaya'}) 

        user_data = json.dumps({'email': 'dan@gmail.com',
                                  'password': 'ulembaya'}) 



class GoodRequestTestCase(ParcelsTestCase):
    """This class tests views with valid requests"""

    def test_create_order(self):
        """Tests POST /parcels"""
        response = self.client.post('/api/v1/parcels',
                    data=json.dumps(self.order), content_type='application/json', headers={'token': user_token} )
        
        self.assertEqual(json.loads(response.data), {'message': 'Order created'} )
        self.assertEqual(response.status_code, 201)


    def test_admin_change_order_status(self):
        """Tests PUT /parcels/<id>"""
        response = self.client.put('api/v1/parcels/321', headers={'token': admin_token})
        self.assertEqual(response.status_code, 200)

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        response = self.client.put('api/v1/parcels/321/cancel', headers={'token': user_token})
        self.assertEqual(response.status_code, 200)


    def test_get_all_orders(self):
        """Tests GET /parcels"""
        response = self.client.get('api/v1/parcels', headers={'token': admin_token})
        self.assertEqual(response.status_code, 200)
        

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        response = self.client.get('api/v1/users/103/parcels', headers={'token': user_token})
        data = json.loads(response.data)
        
        self.assertEqual(data, users_orders)

    def test_get_specific_order(self):
        """Tests GET /parcels/<id>"""
        response = self.client.get('api/v1/parcels/321', headers={'token': user_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, response_data)

    def test_login(self):
        """Tests Get /login"""
        pass


class BadRequestTestCase(ParcelsTestCase):
    """This class tests views with invalid requests"""

   # def test_create_order(self):
    #    """Tests bad requests to POST /parcels"""
    #    pass

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        response = self.client.put('api/v1/parcels/35420/cancel', headers={'token': user_token}) # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)        
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})

        response = self.client.put('api/v1/parcels/35uh420/cancel', headers={'token': user_token}) # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

    def test_admin_change_order_status(self):
        """Tests bad requests to PUT /parcels/<id>"""
        response = self.client.put('api/v1/parcels/35420', headers={'token': admin_token}) # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)        
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})

        response = self.client.put('api/v1/parcels/35uh420', headers={'token': admin_token}) # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

        

    # def test_get_all_orders(self):
      #  """Tests bad requests to GET /parcels"""
       # pass

    def test_get_all_orders_by_user(self):
        """Tests bad requests to GET /users/<id>/parcels"""
        response = self.client.get('api/v1/users/35530/parcels', headers={'token': user_token})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data), {'message': 'Cannot perform this operation'})

        response = self.client.get('api/v1/users/35fsv530/parcels', headers={'token': user_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})


    def test_get_specific_order(self):
        """Tests bad requests to GET /parcels/<id>"""
        response = self.client.get('api/v1/parcels/24034', headers={'token': user_token})  # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})
        self.assertEqual(response.status_code, 400)

        response = self.client.get('api/v1/parcels/24034u', headers={'token': user_token}) # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Wrong id format'})
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        """Tests bad requests to POST /login"""

        pass


class EdgeCasesTestCase(unittest.TestCase):
    """Tests edge cases"""

    def setUp(self):
        """Set up test variabled"""
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

        
        


    




        

