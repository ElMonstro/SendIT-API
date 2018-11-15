from app.api.v2.views import Parcels, Parcel, CancelOrder, Login
from flask import Blueprint 
from flask_restful import Api 

v2 = Blueprint('v2', __name__, url_prefix='/api/v2')
api = Api(v2)


api.add_resource(Parcels, '/parcels', strict_slashes=False)
api.add_resource(Parcel, '/parcels/<id>', strict_slashes=False)
#api.add_resource(UserParcels, '/users/<id>/parcels', strict_slashes=False)
api.add_resource(CancelOrder, '/parcels/<id>/cancel', strict_slashes=False)
api.add_resource(Login, '/api/v2/auth/login', strict_slashes=False)