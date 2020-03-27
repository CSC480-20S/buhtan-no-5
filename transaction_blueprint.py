from flask import Blueprint
from flask_restful import Api
from endpoints.Deliver import Deliver
from endpoints.Purchase import Purchase
from database import studies
from gui_endpoints import preview_study
from endpoints.Search import Search
from endpoints.IsOwned import IsOwned
from endpoints.GetOwned import GetOwned
from endpoints.GetViewed import GetViewed
from endpoints.GetWishList import GetWishList

trans_bp = Blueprint('transaction', __name__)
api = Api(trans_bp)

api.add_resource(Deliver, '/deliver')
api.add_resource(Purchase, '/purchase')
api.add_resource(studies.EndPointOwnedStudies, '/owned')
api.add_resource(studies.EndPointViewedStudies, '/previewed')
api.add_resource(studies.EndPointWishList, '/wishList')
api.add_resource(preview_study.EndPoint_PreviewStudies, '/studyPreview')
api.add_resource(Search, '/search')
api.add_resource(IsOwned, '/isOwned')
api.add_resource(GetOwned, '/getOwned')
api.add_resource(GetViewed, '/getViewed')
api.add_resource(GetWishList, '/getWishlist')
