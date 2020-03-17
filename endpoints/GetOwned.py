from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class GetOwned(Resource):
    def get(self):
        """"Returns the list of .studies owned by a user.

        Returns all studies owned by a user.

        Args:
            user_id (String): The identifier for the user who owns the studies.

        Returns:
            JSON: The list of owned studies.
        """

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        # print(returned_args)
        connect = connector()["Users"]
        # need to fix this get functions
        user = {"User_id": 1}
        seek = connect.find_one(user)
        search = seek["Owned Studies"]
        print("search is: ", search)
        preview = {'Owned Studies': search}
        return jsonify(preview)