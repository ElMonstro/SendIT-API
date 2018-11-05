from flask import make_response, Blueprint, request
from flask_restful  import Api, Resource


v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1)

orders = {
    321: ['532', '4 5345 343', '4 5343 343', 5, 'In-transit'],
    453: ['352', '4 5435 324', '6 5356 353', 3, 'Delivered'],
    133: ['254', '5 6535 453', '8 5465 742', 6, 'Canceled'],
    301: ['686', '4 5345 343', '4 5343 343', 5, 'In-transit'],
    353: ['350', '4 5435 324', '6 5356 353', 3, 'Delivered'],
    633: ['345', '5 6535 453', '8 5465 742', 6, 'Canceled'],
    365: ['140', '4 5345 343', '4 5343 343', 5, 'In-transit'],
    495: ['675', '4 5435 324', '6 5356 353', 3, 'Delivered'],
    127: ['109', '5 6535 453', '8 5465 742', 6, 'Canceled'],
    249: ['140', '4 5345 343', '4 5343 343', 5, 'In-transit'],
    132: ['619', '4 5435 324', '6 5356 353', 3, 'Delivered'],
    808: ['805', '5 6535 453', '8 5465 742', 6, 'Canceled'],
    809: ['532', '4 5345 343', '4 5343 343', 5, 'In-transit'],
    810: ['352', '4 5435 324', '6 5356 353', 3, 'Delivered'],
    811: ['254', '5 6535 453', '8 5465 742', 6, 'Canceled'],
    812: ['686', '4 5345 343', '4 5343 343', 5, 'In-transit'],
    813: ['350', '4 5435 324', '6 5356 353', 3, 'Delivered'],
    814: ['345', '5 6535 453', '8 5465 742', 6, 'Canceled'],
    815: ['140', '4 5345 343', '4 5343 343', 5, 'In-transit'],
    816: ['675', '4 5435 324', '6 5356 353', 3, 'Delivered'],
    817: ['109', '5 6535 453', '8 5465 742', 6, 'Canceled'],
    818: ['140', '4 5345 343', '4 5343 343', 5, 'In-transit'],
    819: ['619', '4 5435 324', '6 5356 353', 3, 'Delivered'],
    820: ['805', '5 6535 453', '8 5465 742', 6, 'Canceled']
}


class Parcels(Resource):
    def get(self):
        return '' 
    
    def post(self):
        order_no = 100
        data = request.get_json()
        data_list = data['order']
        orders[order_no] = data_list
        return {'messsage': 'Order created'}, 201

class Parcel(Resource):
    def get(self, id):
        return ''
    
    def put(self, id):
        return ''

class UserParcels(Resource):
    def get(self, id):
        return ''


class CancelOrder(Resource):
    def put(self, id):
        return ''


api.add_resource(Parcels, '/parcels')
api.add_resource(Parcel, '/parcels/<id>')
api.add_resource(UserParcels, '/<id>/parcels')
api.add_resource(CancelOrder, '/parcel/<id>/cancel')


