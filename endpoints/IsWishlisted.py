from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class IsWishlisted(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Returns the wish list status of the study.

            Returns true only if the indicated user wishes for the indicated study,
            otherwise returns false.

            Args:
                user_id (String): The identifier for the user who may wish for the study.
                study_id (int): The identifier for the study the user may wish for.

            Returns:
                JSON: true, false, or an error message.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        #parser.add_argument("user_id", type=str, required=True, help="The user ID of the potential owner is a String.")
        parser.add_argument("study_id", type=int, required=True, help="The study ID of the potentially owned study is an integer.")
        returned_args = parser.parse_args()
        user_id = kwargs["user_id"]  #returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)
        # let the helper method handle the database call
        return jsonify(Auxiliary.isWishlisted(user_id, study_id))