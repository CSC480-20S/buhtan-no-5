from flask import Blueprint
from flask_restful import Api
from application.endpoints.Deliver import Deliver
from application.endpoints.Purchase import Purchase
from application.endpoints.Search import Search
from application.endpoints.IsOwned import IsOwned
from application.endpoints.GetOwned import GetOwned
from application.endpoints.GetViewed import GetViewed
from application.endpoints.GetWishList import GetWishList
from application.endpoints.Upload import Upload
from application.endpoints.GetAdminDetails import GetAdminDetails
from application.endpoints.GetPending import GetPending
from application.endpoints.ReviewPending import ReviewPending
from application.endpoints.GetPreview import GetPreview
from application.endpoints.suggestions import TextSuggestion
from application.endpoints.AddWishlist import AddWishlist
from application.endpoints.RemoveWishlist import RemoveWishlist
from application.endpoints.IsWishlisted import IsWishlisted
from application.endpoints.RateStudy import RateStudy
from application.endpoints.GetNotifications import GetNotifications
from application.endpoints.Unpublish import Unpublish
from application.endpoints.CheckToken import CheckToken

trans_bp = Blueprint('transaction', __name__)
api = Api(trans_bp)

api.add_resource(Deliver, '/deliver')
api.add_resource(Purchase, '/purchase')
api.add_resource(Search, '/search')
api.add_resource(IsOwned, '/isOwned')
api.add_resource(GetOwned, '/getOwned')
api.add_resource(GetViewed, '/getViewed')
api.add_resource(GetWishList, '/getWishlist')
api.add_resource(Upload, '/upload')
api.add_resource(GetAdminDetails, '/getAdminDetails')
api.add_resource(GetPending, '/getPending')
api.add_resource(ReviewPending, '/reviewPending')
api.add_resource(GetPreview, '/getPreview')
api.add_resource(TextSuggestion, '/suggestion')
api.add_resource(AddWishlist, '/addWishlist')
api.add_resource(RemoveWishlist, '/removeWishlist')
api.add_resource(IsWishlisted, '/isWishlisted')
api.add_resource(RateStudy, '/rateStudy')
api.add_resource(GetNotifications, "/getNotifications")
api.add_resource(Unpublish, "/unpublish")
api.add_resource(CheckToken, "/checkToken")
