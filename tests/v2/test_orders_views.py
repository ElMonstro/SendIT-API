import os
import unittest
from app import create_app
import json
from app.api.v2.models.user_models import Users
from .mock_data import mock_data, message
from app.db_config import DbConnect


class ParcelsTestCase(unittest.TestCase):
    """Parent Testcase class"""

    def setUp(self):
        """Sets up test variables"""
        self.app = create_app(config='test')
        self.client = self.app.test_client()
        self.app.testing = True
        self.db_conn = DbConnect('test')
        self.order = mock_data['order']
        data = json.dumps(mock_data['admin'])
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        self.admin_token_dict = {'token': json.loads(response.data)['token']}
        data = json.dumps(mock_data['user'])
        response = self.client.post(
            'api/v2/auth/login', content_type="application/json", data=data)
        self.user_token_dict = {'token': json.loads(response.data)['token']}

        self.client.post('api/v2/parcels', data=json.dumps(self.order),
                         headers=self.user_token_dict, content_type="application/json")


class GoodRequestTestCase(ParcelsTestCase):
    """This class tests views with valid requests"""

    def test_create_order(self):
        """Tests good requests to POST /parcels"""
        # Test with valid data format and right auth token
        response = self.client.post('/api/v2/parcels',
                                    data=json.dumps(self.order), content_type='application/json', headers=self.user_token_dict)
        self.assertTrue('order' in json.loads(response.data))
        self.assertEqual(json.loads(response.data)['message'], 'Order created')
        self.assertEqual(response.status_code, 201)

    def test_admin_change_order_status(self):
        """Tests PUT /parcels/<id>Cancel/"""
        self.client.post('api/v2/parcels', data=json.dumps(self.order),
                         headers=self.user_token_dict, content_type="application/json")
        # Test with the right auth token
        last_rec = self.db_conn.get_last_record_id()
        response = self.client.put(
            'api/v2/parcels/{}/deliver'.format(last_rec), headers=self.admin_token_dict)
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Order delivered')
        self.assertTrue('order' in json.loads(response.data))
        self.assertEqual(response.status_code, 200)

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        # Test with the right auth token
        self.client.post(
            'api/v2/parcels', data=json.dumps(mock_data['order']), headers=self.user_token_dict)
        last_rec = self.db_conn.get_last_record_id()
        response = self.client.put(
            'api/v2/parcels/{}/cancel'.format(last_rec), headers=self.user_token_dict)
        self.assertTrue('order' in json.loads(response.data))
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Order canceled')
        self.assertEqual(response.status_code, 200)

    def test_get_all_orders(self):
        """Tests GET /parcels"""
        # Test with the right token
        response = self.client.get(
            'api/v2/parcels', headers=self.admin_token_dict)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data[message], 'All orders fetched')
        self.assertTrue('orders' in data)

    def test_get_all_orders_by_user(self):
        """Tests GET /users/<id>/parcels"""
        # Test with the right token
        response = self.client.get(
            'api/v2/users/2/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertTrue('orders' in data)
        self.assertEqual(response.status_code, 200)

    def test_get_specific_order(self):
        """Tests GET /parcels/<id>"""
        # Test with right auth token
        last_rec = self.db_conn.get_last_record_id()
        response = self.client.get(
            'api/v2/parcels/{}'.format(last_rec), headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('order' in data)

    def test_change_curr_location(self):
        """Tests PUT /parcels/<id>/PresentLocation"""
        # Test with  with valid data
        self.client.post('api/v2/parcels/', data=json.dumps(self.order),
                         headers=self.user_token_dict, content_type="application/json")
        last_rec = self.db_conn.get_last_record_id()
        data = json.dumps({"curr_location": "Nairobi"})
        response = self.client.put(
            'api/v2/parcels/{}/PresentLocation'.format(last_rec), data=data, headers=self.admin_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Present location changed')
        self.assertTrue('order' in json.loads(response.data))
        self.assertEqual(response.status_code, 200)

    def test_change_dest_location(self):
        """Tests PUT /parcels/<id>/PresentLocation"""
        # Test with  with valid data
        self.client.post('api/v2/parcels/', data=json.dumps(self.order),
                         headers=self.user_token_dict, content_type="application/json")
        last_rec = self.db_conn.get_last_record_id()
        data = json.dumps({"dest_location": "12345678"})
        response = self.client.put(
            'api/v2/parcels/{}/destination'.format(last_rec), data=data, headers=self.user_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Destination location changed')
        self.assertTrue('order' in json.loads(response.data))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Clear database records"""
        self.db_conn.delete_all_orders()


class BadRequestTestCase(ParcelsTestCase):
    """This class tests views with invalid requests"""

    def test_create_order(self):
        """Tests bad requests to POST /parcels"""
        # Test with wrong data type
        response = self.client.post('/api/v2/parcels',
                                    data=json.dumps(['jay', 'bad', 'data']), content_type='application/json', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {'message': 'Payload must be a dictionary(object)'})

    def test_cancel_order(self):
        """Tests PUT /parcels/<id>/cancel"""
        # Test unregistered id
        # Correct format but not there
        response = self.client.put(
            'api/v2/parcels/35420/cancel', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {'message': 'No Parcel delivery order with that id'})
        # Test invalid format id
        response = self.client.put(
            'api/v2/parcels/35uh420/cancel', headers=self.user_token_dict)  # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})

    def test_admin_change_order_status(self):
        """Tests bad requests to PUT /parcels/<id>"""
        # Test unregistered id
        # Correct format but not there
        response = self.client.put(
            'api/v2/parcels/35420/deliver', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data, {'message': 'No Parcel delivery order with that id'})
        # Test invalid format id
        response = self.client.put(
            'api/v2/parcels/35uh420/deliver', headers=self.admin_token_dict)  # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})
        # test with delivered parcel
        self.client.post('api/v2/parcels', data=json.dumps(self.order),
                         headers=self.user_token_dict, content_type="application/json")
        last_rec = self.db_conn.get_last_record_id()
        self.client.put(
            'api/v2/parcels/{}/deliver'.format(last_rec), headers=self.admin_token_dict)
        response = self.client.put(
            'api/v2/parcels/{}/deliver'.format(last_rec), headers=self.admin_token_dict)
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Unsuccesful, order already delivered')
        self.assertEqual(response.status_code, 400)

    # def test_get_all_orders(self):
      #  """Tests bad requests to GET /parcels"""
       # pass

    def test_change_curr_location(self):
        """Tests PUT requests to api/v2/parcels/<id>/PresentLocation """
        self.client.post('api/v2/parcels/', data=json.dumps(self.order),
                         headers=self.user_token_dict, content_type="application/json")
        last_rec = self.db_conn.get_last_record_id()
        # Test with user token
        response = self.client.put(
            'api/v2/parcels/{}/PresentLocation'.format(last_rec), headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(
            data, {message: 'You are not authorized to perform this operation'})
        self.assertEqual(response.status_code, 403)
        # Test invalid format id
        response = self.client.put(
            'api/v2/parcels/35uh420/PresentLocation', headers=self.admin_token_dict)  # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})
        # Test with  with string
        data = json.dumps("dest_location")
        response = self.client.put(
            'api/v2/parcels/{}/PresentLocation'.format(last_rec), data=data, headers=self.admin_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Current Location must be in an object')
        self.assertEqual(response.status_code, 400)
        # Test with no curr_loc key
        data = json.dumps({"dest_location": 'fdtg'})
        response = self.client.put(
            'api/v2/parcels/{}/PresentLocation'.format(last_rec), data=data, headers=self.admin_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'curr_location key not in object')
        self.assertEqual(response.status_code, 400)
        # Test for orders already delivered
        self.client.put(
            'api/v2/parcels/{}/deliver'.format(last_rec), headers=self.admin_token_dict)
        data = json.dumps({"curr_location": "12345678"})
        response = self.client.put(
            'api/v2/parcels/{}/PresentLocation'.format(last_rec), data=data, headers=self.admin_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Unsuccesful, order already delivered')
        self.assertEqual(response.status_code, 400)
        # Test with bogus parcel id
        response = self.client.put(
            'api/v2/parcels/2342214/PresentLocation', data=data, headers=self.admin_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'No parcel order with that id')
        self.assertEqual(response.status_code, 404)

    def test_change_dest_location(self):
        """Tests PUT requests to api/v2/parcels/<id>/destination """
        self.client.post('api/v2/parcels/', data=json.dumps(self.order),
                         headers=self.user_token_dict, content_type="application/json")
        last_rec = self.db_conn.get_last_record_id()
        # Test with user token
        response = self.client.put(
            'api/v2/parcels/{}/destination'.format(last_rec), headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(
            data, {message: 'You are not authorized to perform this operation'})
        self.assertEqual(response.status_code, 403)
        # Test invalid format id
        response = self.client.put(
            'api/v2/parcels/35uh420/destination', headers=self.user_token_dict)  # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})
        # Test with  with string data
        data = json.dumps("dest_location")
        response = self.client.put(
            'api/v2/parcels/{}/destination'.format(last_rec), data=data, headers=self.user_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Destination Location must be in an object')
        self.assertEqual(response.status_code, 400)
        # Test with no dest_location key
        data = json.dumps({"c_location": 'fdtg'})
        response = self.client.put(
            'api/v2/parcels/{}/destination'.format(last_rec), data=data, headers=self.user_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'dest_location key not in object')
        self.assertEqual(response.status_code, 400)
        # Test for orders already delivered
        self.client.put(
            'api/v2/parcels/{}/deliver'.format(last_rec), headers=self.admin_token_dict)
        data = json.dumps({"dest_location": "12345678"})
        response = self.client.put(
            'api/v2/parcels/{}/destination'.format(last_rec), data=data, headers=self.user_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'Unsuccesful, order already delivered')
        self.assertEqual(response.status_code, 400)
        # Test with bogus parcel id
        response = self.client.put(
            'api/v2/parcels/2342214/destination', data=data, headers=self.user_token_dict, content_type="application/json")
        self.assertEqual(json.loads(response.data)[
                         'message'], 'No parcel order with that id')
        self.assertEqual(response.status_code, 404)

    def test_get_all_orders_by_user(self):
        """Tests bad requests to GET /users/<id>/parcels"""
        # Test with accessing other users parcels
        response = self.client.get(
            'api/v2/users/35530/parcels', headers=self.user_token_dict)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.data), {
                         'message': 'You are not authorized to perform this operation'})
        # Test with wrong format user id
        response = self.client.get(
            'api/v2/users/35fsv530/parcels', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'message': 'Wrong id format'})
        # Test with user with no orders
        response = self.client.get(
            'api/v2/users/104/parcels', headers=self.admin_token_dict)
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'No orders by that user'})
        self.assertEqual(response.status_code, 404)

    def test_get_specific_order(self):
        """Tests bad requests to GET /parcels/<id>"""
        # Test with wrong parcel id
        # Correct format but not there
        response = self.client.get(
            'api/v2/parcels/24034', headers=self.user_token_dict)
        data = json.loads(response.data)
        self.assertEqual(
            data, {'message': 'No Parcel delivery order with that id'})
        self.assertEqual(response.status_code, 404)
        # Test with wrong parcel id format
        response = self.client.get(
            'api/v2/parcels/24034u', headers=self.user_token_dict)  # Incorrect id format
        data = json.loads(response.data)
        self.assertEqual(data, {'message': 'Wrong id format'})
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """Clear database records"""
        self.db_conn.delete_all_orders()
