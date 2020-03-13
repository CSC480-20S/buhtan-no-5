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
            A user id is required to verify the request is valid.
            All other parameters are optional.
            If title is given, return only studies with that title.
            If keywords are given, return only studies with all of those keywords.
            If keyword_all is false, each study need only have one or more keywords, not necessarily all of them.
            If limit is given, no more than limit studies will be returned.
            ...in progress.

            Args:
                user_id (String): The identifier for the user trying to search. Will be used for confirming access permission.
                title (String): The identifier for the study the user is trying to purchase.
                keywords (String): Contains all the keywords that a study must have.
                keyword_separator (String): Separates the keywords in the keywords parameter. Defaults to |.
                keyword_all (Boolean): If false, any non-empty subset of the keywords is sufficient to match.
                limit (Integer): The maximum number of studies to return. Defaults to unlimited when missing or negative.


            Returns:
                JSON: The list of studies that meet the specified requirements.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        parser.add_argument("title", type=str)
        parser.add_argument("keywords", type=str)
        parser.add_argument("keyword_separator", type=str)
        parser.add_argument("keyword_all", type=bool)
        parser.add_argument("limit", type=int)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        title = returned_args.get("title", None)
        keywords_unsplit = returned_args.get("keywords", None)
        keyword_separator = returned_args.get("keyword_separator", "|")
        keyword_all = returned_args.get("keyword_all", True)
        limit = returned_args.get("limit", -1)
        # verify the required parameters exist
        if user_id == None:
            return jsonify({"error": "missing user_id parameter"})
        # get the necessary data from the database
        # this exists for verifying we have an authenticated user
        user = Purchase.getUser(user_id)
        #should make some check that the user's session is still valid
        #i.e. last authentication within 30 minutes

        # build search parameters
        params = {}
        if title != None:
            params["Title"] = title
        if keywords_unsplit != None:
            keywords = keywords_unsplit.split(keyword_separator)
            #intersection/and
            if keyword_all == True:
                params["Keywords"] = {"$all": keywords}
            #union/or
            else:
                params["Keywords"] = { "$in": keywords}
        # query database
        studyList = getStudies(params, limit)
        # convert output
        out = {}
        for i in range(len(studyList)):
            out[str(i)] = studyList[i].build_dict()
        # return converted output
        return jsonify(out)

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

    studyList = []
    #not sure if this actually returns a list
    for study in seek[0:numStudies]:
        studyList.append(f5study(study_id, seek["Title"], seek["Author"], seek["CostinCredits"], seek["Purpose"], seek["References"],
                seek["Categories"], seek["Sub_Categories"], seek["Keywords"], seek["Num_Stimuli"],
                seek["Num_Responses"], seek["Randomize"], seek["Duration"], seek["Num_trials"], seek["Rating"],
                seek["Institution"], "Template redacted"))
    return studyList
