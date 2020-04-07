from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from endpoints import Auxiliary
from database import studies
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy


class Recommendation(Resource):

    @Auxiliary.auth_dec
    def get(self):
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str, required=True,
                            help="The user_id is string representation of user's ID.")
        returned_args = parser.parse_args()

        user_id = returned_args.get("user_id", None)
        user = Auxiliary.getUser(user_id)
        print(set(user.get_ownedStudies())) # unique set of studies owned
        # owned = studies.EndPointOwnedStudies.get(user_id)
        # print("bllahh: " + owned)
        return user.get_ownedStudies()
    # viewed = studies.EndPointViewedStudies.get(user_id)
    # print(studies.EndPointWishList.get(user_id).split(','))

    # print(studies.EndPointWishList.get(user_id).split(','))
    #  uniques = set().union(owned, viewed, wished)  # unique list to test for values being present/non duplicate
    # print(len(uniques))
    # if len(uniques) <= 0:
    #     return None   # presumably a first time user can't have recomendations, it would just be the top rated list.

    #  return jsonify({"list": uniques})
