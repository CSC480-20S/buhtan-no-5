from flask import jsonify
from flask_restful import Resource, reqparse
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary


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
        parser.add_argument("user_id", type=str, required=True, help="An active user ID must be provided.")
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
        # verify the required parameters exist - now handled by add_argument
        #if user_id == None:
        #    return jsonify({"error": "missing user_id parameter"})
        # get the necessary data from the database
        # this exists for verifying we have an authenticated user
        user = Auxiliary.getUser(user_id)
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
        studyList = Auxiliary.getStudies(params, limit)
        # convert output
        out = {}
        for i in range(len(studyList)):
            out[i] = studyList[i].build_dict()
        # return converted output
        return jsonify(out)

