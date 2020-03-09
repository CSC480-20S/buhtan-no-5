from flask import jsonify
from flask_restful import Resource, reqparse
from database import DbConnection
from studystore import FindingFiveStudyStoreStudy ,FindingFiveStudyStoreUser

class Purchase(Resource):
    def get(self):
        """"Establishes an owns relationship between a study and a user.

            Establishes the owns relationship only if the user has sufficient credits and doesn't already own the study.

            Args:
                user_id (String): The identifier for the user trying to purchase the study.
                study_id (int): The identifier for the study the user is trying to purchase.
                credits_available (int): The current credit balance for the user. Overrides any stored balance.

            Returns:
                JSON: The cost of the study, or an error message.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        parser.add_argument("study_id", type=int)
        parser.add_argument("credits_available", type=int)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)
        credits_available = returned_args.get("credits_available", None)
        # verify the parameters exist
        if user_id == None or study_id == None or credits_available == None:
            return jsonify({"error": "missing parameter"})
        # get the necessary data from the database
        user = self.getUser(user_id)
        study = self.getStudy(study_id)
        cost = study.get_costInCredits()
        # check for sufficient credits and not already owning the study
        if cost > credits_available:
            return jsonify({"error": "insufficient credits"})
        elif study_id in user.get_ownedStudies():
            return jsonify({"error": "user already owns study"})
        # update the user data
        user.set_numCredits(credits_available - cost)
        user.set_ownedStudies(user.get_ownedStudies() + [study_id])
        self.updateUser(user)
        # return the cost
        return jsonify({"cost": cost})

    def getStudy(study_id):

        """Grabs a study given its ID.

        Pulls from the database and returns a FindingFiveStudyStoreStudy object.

        Args:
            study_id (int): The ID assigned to a study at upload.

        Returns:
            FindingFiveStudyStoreStudy: The associated study in the database.
        """
        # I assume this call returns a dict().
        #study = DbConnection.get("studies", study_id)
        #return FindingFiveStudyStoreStudy(study["id"], study["title"], study["author"], study["cost"])

        # take: two - pulling from Shawn's code example
        connect = connector()["Studies"]
        study = {"Study_id" : study_id}
        seek = connect.find_one(study)
        return FindingFiveStudyStoreStudy(study_id, seek["Title"], seek["Author"], seek["CostinCredits"], seek["Purpose"], seek["References"], seek["Categories"], seek["Sub_Categories"], seek["Keywords"], seek["Num_Stimuli"], seek["Num_Responses"], seek["Randomize"], seek["Duration"], seek["Num_trials"], seek["Rating"], seek["Institution"], seek["Template"])

    def getUser(user_id):
        """Grabs a user given its ID.

            Pulls from the database and returns a FindingFiveStudyStoreUser object.

            Args:
                user_id (String): The ID associated with a user at authentication.

            Returns:
                FindingFiveStudyStoreUser: The associated user in the database.
            """
        # I assume this call returns a dict().
        #user = DbConnection.get("users", user_id)
        #return FindingFiveStudyStoreUser(user["id"], user["num_credits"], user["owned_studies"], user["viewed_studies"])

        #take: two - pulling from Shawn's code example
        connect = connector()["Users"]
        user = {"User_id": user_id}
        seek = connect.find_one(user)
        return FindingFiveStudyStoreUser(user_id, seek["Num Credits"], seek["Owned Studies"], seek["Viewed Studies"])

    def updateUser(user):
        """"Updates a user in the database.

        Pushes a new version of the user data into the database. Assumes the current ID already exists.

        Args:
            user (FindingFiveStudyStoreUser): The new data to write to the database.

        Returns:
            Nothing.
        """
        #userDict = {}
        #userDict["id"] = user.get_userId()
        #userDict["num_credits"] = user.get_numCredits()
        #userDict["owned_studies"] = user.get_ownedStudies()
        #userDict["viewed_studies"] = user.get_viewedStudies()
        #DbConnection.edit("users", userDict["id"], userDict)

        # take: two - pulling from Shawn's code example
        connect = connector()["Users"]
        userJ = {"User_id": user.get_userId()}
        connect.update_one(userJ, {"Num Credits": user.get_numCredits()})
        listerO = {"$set": {"Owned Studies": user.get_ownedStudies()}}
        connect.update_one(userJ, listerO)
        listerV = {"$set": {"Viewed Studies": user.get_viewedStudies()}}
        connect.update_one(userJ, listerV)
