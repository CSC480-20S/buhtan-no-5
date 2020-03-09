from flask import jsonify
from flask_restful import Resource, reqparse
from database import DbConnection
from studystore import FindingFiveStudyStoreStudy ,FindingFiveStudyStoreUser
import Purchase

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
        #obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        parser.add_argument("study_id", type=int)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)
        #verify the parameters exist
        if user_id == None or study_id == None:
            return jsonify({"error":"missing parameter"})
        #get the necessary data from the database
        user = Purchase.getUser(user_id)
        study = Purchase.getStudy(study_id)
        #return the study only if owned
        if study_id in user.get_ownedStudies():
            return study.get_template()
        else:
            return jsonify({"error":"user does not own study"})
