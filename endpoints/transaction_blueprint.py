from flask import Blueprint
from flask_restful import Api
from endpoints.Deliver import Deliver
from endpoints.Purchase import Purchase
from database import studies
from gui_endpoints import preview_study
from endpoints.Search import Search

trans_bp = Blueprint('transaction',__name__)
api =Api(trans_bp)

api.add_resource(Deliver,'/deliver')
api.add_resource(Purchase, '/purchase')
api.add_resource(studies.EndPointOwnedStudies,'/owned')
api.add_resource(studies.EndPointViewedStudies,'/previewed')
api.add_resource(preview_study.EndPoint_PreviewStudies,'/studyPreview')
api.add_resource(Search, '/search')
