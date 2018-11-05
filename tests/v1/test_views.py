import unittest
from run import app
import json

class ParcelsTestCase(unittest.TestCase):
    """Parent Testcase class"""
    def setUp(self):
        """Sets up test variables"""
        pass

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





        

