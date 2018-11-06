from app.api.v1.views import Parcels, Parcel, CancelOrder, UserParcels
from flask import Blueprint
from flask_restful import Api

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1)




api.add_resource(Parcels, '/parcels', strict_slashes=False)
api.add_resource(Parcel, '/parcels/<id>', strict_slashes=False)
api.add_resource(UserParcels, '/users/<id>/parcels', strict_slashes=False)
api.add_resource(CancelOrder, '/parcels/<id>/cancel', strict_slashes=False)