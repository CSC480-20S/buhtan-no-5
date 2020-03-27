from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class GetOwned(Resource):
    @Auxiliary.auth_dec
    def get(self):
        """"Returns the list of .studies owned by a user.

        Returns all studies owned by a user.

        Args:
            user_id (String): The identifier for the user who owns the studies.

        Returns:
            JSON: The list of owned studies.
        """

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str, required=True, help="The user ID of the owner is a String.")
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        # print(returned_args)
        user = Auxiliary.getUser(user_id)
        search = user.get_ownedStudies()
        params = {"Study_id": {"$in": search}}
        studyList = Auxiliary.getStudies(params)
        # convert output
        out = {}
        for i, study in enumerate(studyList):
            out[i] = study.build_dict()
        # return converted output
        return jsonify(out)
