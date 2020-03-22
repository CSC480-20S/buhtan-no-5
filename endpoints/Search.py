from flask import jsonify
from flask_restful import Resource, reqparse
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary


class Search(Resource):
    @Auxiliary.auth_dec
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
        parser.add_argument("title", type=str)
        parser.add_argument("keywords", type=str)
        parser.add_argument("keyword_separator", type=str, default="|")
        parser.add_argument("keyword_all", type=bool, default=True)
        parser.add_argument("limit", type=int, default=-1)

        # the second parameter to each method call is purely for consistency,
        # they don't actually do anything. They should match the defaults above.
        returned_args = parser.parse_args()
        title = returned_args.get("title", None)
        keywords_unsplit = returned_args.get("keywords", None)
        keyword_separator = returned_args.get("keyword_separator", "|")
        keyword_all = returned_args.get("keyword_all", True)
        limit = returned_args.get("limit", -1)

        # build search parameters
        params = {}
        if title is not None:
            params["Title"] = title
        if keywords_unsplit is not None:
            keywords = keywords_unsplit.split(keyword_separator)
            # intersection/and
            if keyword_all is True:
                params["Keywords"] = {"$all": keywords}
            # union/or
            else:
                params["Keywords"] = {"$in": keywords}
        # query database
        studyList = Auxiliary.getStudies(params, limit)
        # convert output
        out = {}
        for i, study in enumerate(studyList):
            out[i] = study.build_dict()
        # return converted output
        return jsonify(out)
