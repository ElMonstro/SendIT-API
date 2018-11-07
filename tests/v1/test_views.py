import unittest
from run import app
import json

order = {'order': ['532', '4 5345 343', '4 5343 343', 5, 'In-transit']}
response_data = {"order": { "321": [532, "4 5345 343", "4 5343 343", 5, "Canceled"]}}

users_orders = {
    "orders": {
        "353": [350, "4 5435 324", "6 5356 353", 3, "Delivered" ],
        "813": [350, "4 5435 324", "6 5356 353", 3,  "Delivered"]
    }
}

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

    def test_admin_change_order_status(self):
        """Tests PUT /parcels/<id>"""
        response = self.client.put('api/v1/parcels/321')
        self.assertEqual(response.status_code, 200)

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        response = self.client.put('api/v1/parcels/321/cancel')
        self.assertEqual(response.status_code, 200)


    def test_get_all_orders(self):
        """Tests GET /parcels"""
        response = self.client.get('api/v1/parcels')
        self.assertEqual(response.status_code, 200)
        

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        response = self.client.get('api/v1/users/350/parcels')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, users_orders)

    def test_get_specific_order(self):
        """Tests GET /parcels/<id>"""
        response = self.client.get('api/v1/parcels/321')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, response_data)


class BadRequest(ParcelsTestCase):
    """This class tests views with invalid requests"""

   # def test_create_order(self):
    #    """Tests bad requests to POST /parcels"""
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

    def test_admin_change_order_status(self):
        """Tests bad requests to PUT /parcels/<id>"""
        response = self.client.put('api/v1/parcels/35420') # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)        
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})

        response = self.client.put('api/v1/parcels/35uh420') # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

        

    # def test_get_all_orders(self):
      #  """Tests bad requests to GET /parcels"""
       # pass

    def test_get_all_orders_by_user(self):
        """Tests bad requests to GET /users/<id>/parcels"""
        response = self.client.get('api/v1/users/35530/parcels')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'message': 'No orders by that user'})

    def test_get_specific_order(self):
        """Tests bad requests to GET /parcels/<id>"""
        response = self.client.get('api/v1/parcels/24034')  # Correct format but not there
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'No Parcel delivery order with that id'})
        self.assertEqual(response.status_code, 400)

        response = self.client.get('api/v1/parcels/24034u') # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Wrong id format'})
        self.assertEqual(response.status_code, 400)


    




        

