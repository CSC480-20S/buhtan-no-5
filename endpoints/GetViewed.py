from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class GetViewed(Resource):
    def get(self):
        """"Returns the list of .studies viewed by a user.

        Returns all studies viewed by a user.

        Args:
            user_id (String): The identifier for the user who has viewed the studies.

        Returns:
            JSON: The list of viewed studies.
        """

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str, required=True, help="The user ID of the viewer is a String.")
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        # print(returned_args)
        connect = connector()["Users"]
        # need to fix this get functions
        user = {"User_id": user_id}
        seek = connect.find_one(user)
        search = seek["Viewed Studies"]
        params = {"Study_id": {"$in": search}}
        studyList = Auxiliary.getStudies(params)
        # convert output
        out = {}
        for i in range(len(studyList)):
            out[i] = studyList[i].build_dict()
        # return converted output
        return jsonify(out)