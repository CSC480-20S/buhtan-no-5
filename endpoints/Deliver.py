from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class Deliver(Resource):
    def get(self):
        """"Returns the study template.

            Returns the template of the indicated study only if the indicated user owns that study.

            Args:
                user_id (String): The identifier for the user trying to download the template.
                study_id (int): The identifier for the study the user is trying to download.

            Returns:
                JSON: The desired study template, or an error message.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str, required=True, help="The user ID of the owner is a String.")
        parser.add_argument("study_id", type=int, required=True, help="The study ID of the owned study is an integer.")
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)
        # return the study template only if owned
        if Auxiliary.isOwned(user_id, study_id):
            # only acquire study if we own it
            study = Auxiliary.getStudy(study_id)
            return study.get_template()
        else:
            return jsonify({"error": "user does not own study"})
