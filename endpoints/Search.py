from flask import jsonify
from flask_restful import Resource, reqparse
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
import Purchase

class Search(Resource):
    def get(self):
        """"Provides a list of studies from the database.

            Provides a list of studies, in JSON format, that meet some specified requirements.
            If title is given, return all studies with that title.
            ...in progress.

            Args:
                user_id (String): The identifier for the user trying to search. Will be used for confirming access permission.
                title: (String): The identifier for the study the user is trying to purchase.

            Returns:
                JSON: The list of studies that meet the specified requirements.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        parser.add_argument("title", type=str)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        title = returned_args.get("title", None)
        # verify the parameters exist
        # will need to change this to allow title=None when other specifying parameters are given
        if user_id == None or title == None:
            return jsonify({"error": "missing parameter"})
        # get the necessary data from the database
        # this exists for verifying we have an authenticated user
        user = Purchase.getUser(user_id)

        # build search parameters
        params = { "Title":title }
        # query database
        # convert output
        # return converted output
        return jsonify({"Results": {"No results":True}})

def getStudies(params, maxStudies=-1):
    """Grabs a list of studies given some parameters they need to meet.

    Pulls from the database and returns a list of FindingFiveStudyStoreStudy objects.
    Each object will have the fields given in params equal to the values paired with them in params.

    Args:
        params (dict): Pairs field names with the values they must have.
        maxStudies (int): If greater than or equal to zero, no more than max studies will be in the output list.

    Returns:
        list<FindingFiveStudyStoreStudy>: The first "max" studies that have the given params.
    """

    #if asked for zero studies, just return
    if (maxStudies == 0):
        return []
    #change to the number the Mongo code likes uses for no limit
    elif (maxStudies < 0):
        maxStudies == 0

    #acquire studies
    connect = DbConnection.connector()["Studies"]
    seek = connect.find(filter=params, projection={"Template":False}, limit=maxStudies)

    #get the number of studies returned - {} gives us all
    numStudies = seek.collection.count_documents({})

    #not sure if this actually returns a list
    return seek[0:numStudies]