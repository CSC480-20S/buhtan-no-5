from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user


class CheckToken(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Returns the user ID associated with the token.

        Also creates a new user in the database if not already present.
        This function is intended to complement /token/generate,
        given that that endpoint will not be accessible to the GUI.
        It must be called prior to any other user-related endpoints
        to ensure the user is properly initialized.
        The output is in JSON form, rather than a simple String,
        so that other information can be returned if it is added to the token.

        Args:
            user_id (String): The identifier for the user to return.

        Returns:
            JSON: {"user_id": user_id, "new": N} where N is true if a new user was created in the database. (If not, N is false.)
        """
        # obtain parameters
        user_id = kwargs["user_id"]
        # auxiliary function does all the work
        user_is_new = Auxiliary.createUser(f5user(user_id))
        if user_is_new:
            Auxiliary.addNotification(user_id, "Welcome!", "Thank you for visiting the FindingFive Study Store.", "Welcome")
        # return converted output
        return jsonify({"user_id": user_id, "new": user_is_new})
