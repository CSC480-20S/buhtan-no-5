from flask import jsonify
from flask_restful import Resource, reqparse
from database import DbConnection
from studystore import FindingFiveStudyStoreStudy ,FindingFiveStudyStoreUser


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
        user = self.getUser(user_id)
        study = self.getStudy(study_id)
        #return the study only if owned
        if study_id in user.get_ownedStudies():
            return study.get_template()
        else:
            return jsonify({"error":"user does not own study"})

    def getStudy(study_id):

        """Grabs a study given its ID.

        Pulls from the database and returns a FindingFiveStudyStoreStudy object.

        Args:
            study_id (int): The ID assigned to a study at upload.

        Returns:
            FindingFiveStudyStoreStudy: The associated study in the database.
        """
    # I assume this call returns a dict().
        study = DbConnection.get("studies", study_id)
        return FindingFiveStudyStoreStudy(study["id"], study["title"], study["author"], study["cost"])


    def getUser(user_id):
        """Grabs a user given its ID.

            Pulls from the database and returns a FindingFiveStudyStoreUser object.

            Args:
                user_id (String): The ID associated with a user at authentication.

            Returns:
                FindingFiveStudyStoreUser: The associated user in the database.
            """
        # I assume this call returns a dict().
        user = DbConnection.get("users", user_id)
        return FindingFiveStudyStoreUser(user["id"], user["num_credits"], user["owned_studies"], user["viewed_studies"])


    def updateUser(user):
        """"Updates a user in the database.

        Pushes a new version of the user data into the database. Assumes the current ID already exists.

        Args:
            user (FindingFiveStudyStoreUser): The new data to write to the database.

        Returns:
            Nothing.
        """
        userDict = {}
        userDict["id"] = user.get_userId()
        userDict["num_credits"] = user.get_numCredits()
        userDict["owned_studies"] = user.get_ownedStudies()
        userDict["viewed_studies"] = user.get_viewedStudies()
        DbConnection.edit("users", userDict["id"], userDict)
