import unittest
from run import app
import json

order = {'order': ['532', '4 5345 343', '4 5343 343', 5, 'In-transit']}
response_data = {"order": { "321": ["532", "4 5345 343", "4 5343 343",
            5,
            "In-transit"
        ]
    }}

class ParcelsTestCase(unittest.TestCase):
    """Parent Testcase class"""
    def setUp(self):
        """Sets up test variables"""
        self.app = app
        self.client = self.app.test_client(self)
        self.app.testing = True
        self.order = order


class GoodRequest(ParcelsTestCase):
    """This class tests views with valid requests"""

    def test_create_order(self):
        """Tests POST /parcels"""
        response = self.client.post('/api/v1/parcels',
                    data=json.dumps(self.order), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'messsage': 'Order created'} )

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        response = self.client.put('api/parcels/350/cancel')
        self.assertEqual(response.status_code, 204)

    def test_get_all_orders(self):
        """Tests GET /parcels"""
        response = self.client.get('api/v1/parcels')
        self.assertEqual(response.status_code, 200)
        

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        response = self.client.get('api/v1/users/350/parcels')
        self.assertEqual(response.status_code, 200)

    def test_get_specific_order(self):
        """Tests GET /parcels/<id>"""
        response = self.client.get('api/v1/parcels/321')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, response_data)


class BadRequest(ParcelsTestCase):
    """This class tests views with invalid requests"""
   # def test_create_order(self):
    #    """Tests bad requests with POST /parcels"""
    #    pass

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        response = self.client.put('api/v1/parcels/35420/cancel') # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)        
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})

        response = self.client.put('api/v1/parcels/35uh420/cancel') # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

        

    # def test_get_all_orders(self):
      #  """Tests bad requests with GET /parcels"""
       # pass

    def test_get_all_orders_by_user(self):
        """Tests bad requests with GET /users/<id>/parcels"""
        response = self.client.get('/users/35053/parcels')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'No user with that order id'})

    def test_get_specific_order(self):
        """Tests bad requests with GET /parcels/<id>"""
        response = self.client.get('api/v1/parcels/24034')  # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})
        self.assertEqual(response.status_code, 400)

        response = self.client.get('api/v1/parcels/24034u') # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Wrong id format'})
        self.assertEqual(response.status_code, 400)

    




        

