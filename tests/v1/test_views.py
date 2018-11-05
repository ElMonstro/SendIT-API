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


class KnownValues(ParcelsTestCase):
    """This class tests views with valid requests"""

    def test_create_order(self):
        """Tests POST /parcels"""
        pass

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        pass

    def test_get_all_orders(self):
        """Tests GET /parcels"""
        pass

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        pass


class UnKnownValues(ParcelsTestCase):
    """This class tests views with invalid requests"""
    def test_create_order(self):
        """Tests POST /parcels"""
        pass

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        pass

    def test_get_all_orders(self):
        """Tests GET /parcels"""
        pass

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        pass





        

