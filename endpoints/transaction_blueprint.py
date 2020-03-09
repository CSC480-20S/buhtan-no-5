from flask import Blueprint
from flask_restful import Api
from endpoints.Deliver import Deliver
from endpoints.Purchase import Purchase
from database import studies
trans_bp = Blueprint('transaction',__name__)
api =Api(trans_bp)

api.add_resource(Deliver,'/deliver')
api.add_resource(Purchase, '/purchase')
api.add_resource(studies.EndPointOwnedStudies,'/owned')
api.add_resource(studies.EndPointViewedStudies,'/previewed')

