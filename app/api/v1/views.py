from flask import request
from flask_restful  import Resource
from app.api.v1.models import ParcelOrders




class Parcels(Resource):
    """Handles requests for the /parcels route"""

    def __init__(self):
        self.db = ParcelOrders()

    def get(self):
        return self.db.get_all_orders()
    
    def post(self):
        data = request.get_json()
        data_list = data['order']
        success = self.db.save(data_list)

        if success:       
            return {'messsage': 'Order created'}, 201
        else:
            return {'message': 'Invalid data format'}


class Parcel(Resource):
    """Handles request for /parcels/<id> route"""

    def __init__(self):
        self.db = ParcelOrders()


    def get(self, id):
        try:
            int_id = int(id)
        except:
            return {'message': 'Wrong id format'}, 400

        order = self.db.get_specific_order(int_id)

        if order:
            return order
        else: 
            return {'message': 'No Parcel delivery order with that id'}, 400
        
    
    def put(self, id):
        try:
            int_id = int(id)
        except:
            return {'message': 'Wrong id format'}, 400

        success = self.db.change_delivery_status(int_id)

        if success:
            return {'message': 'Status changed'} 
        else:       
            return {'message': 'No Parcel delivery order with that id'}, 400


class UserParcels(Resource):
    """Handles the route /users/<user_id>/parcels"""
    
    def __init__(self):
        self.db = ParcelOrders()

    def get(self, id):
        try:
            int_id = int(id)
        except:
            return {'message': 'Wrong id format'}, 400

        orders = self.db.get_all_user_orders(int_id)

        if not  orders:
            return {'message': 'No orders by that user'}, 400
        return orders

            


class CancelOrder(Resource):
    """Handles the route /parcels/<parcel_id>/cancel"""

    def __init__(self):
        self.db = ParcelOrders()

    def put(self, id):
        try:
            int_id = int(id)
        except:
            return {'message': 'Wrong id format'}, 400

        success = self.db.cancel_order(int_id)

        if success:
            return {'message': 'Order canceled'} 
        else:       
            return {'message': 'No Parcel delivery order with that id'}, 400





