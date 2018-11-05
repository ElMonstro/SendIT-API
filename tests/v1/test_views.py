import unittest
from run import app
import json

order = {'order': ['532', '4 5345 343', '4 5343 343', 5, 'In-transit']}

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
        response = self.client.post('/api/v1/orders',
                    data=json.dumps(self.order), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        response = self.client.put('/parcels/350/cancel')
        self.assertEqual(response.status_code, 204)

    def test_get_all_orders(self):
        """Tests GET /parcels"""
        response = self.client.get('/parcels')
        self.assertEqual(response.status_code, 200)
        

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        response = self.client.get('/users/350/parcels')
        self.assertEqual(response.status_code, 200)


class BadRequest(ParcelsTestCase):
    """This class tests views with invalid requests"""
   # def test_create_order(self):
    #    """Tests bad requests with POST /parcels"""
    #    pass

    def test_cancel_order(self):
        """Tests bad requests with PUT /parcels/<id>/cancel"""
        response = self.client.put('/parcels/35240/cancel') # Wrong parcel id
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'No order with that id'})
        

    # def test_get_all_orders(self):
      #  """Tests bad requests with GET /parcels"""
       # pass

    def test_get_all_orders_by_user(self):
        """Tests bad requests with GET /users/<id>/parcels"""
        response = self.client.get('/users/35053/parcels')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'No user with that order id'})
        





        

