from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class Search(Resource):
    @Auxiliary.auth_dec
    @Auxiliary.time_backend
    def get(self):
        """"Provides a list of studies from the database.

            Provides a list of studies, in JSON format, that meet some specified requirements.
            All parameters are optional, except for the token required for authentication.
            Providing none of the optional parameters will result in all studies being returned,
            but may result in a connection time out.
            If title is given, return only studies with that title.
            If keywords are given, return only studies with all of those keywords.
            If keyword_all is false, each study need only have one or more keywords, not necessarily all of them.
            If limit is given, no more than limit studies will be returned.
            If price_min is given, return only studies at that price or higher.
            If price_max is given, return only studies at that price or lower.
            If price_min is greater than price_max, ignore price_max and negative values of price_min.
            For the purposes of this method, the price of a study may be negative.
            ...in progress.

            Args:
                title (String): The identifier for the study the user is trying to purchase.
                keywords (String): Contains all the keywords that a study must have.
                keyword_separator (String): Separates the keywords in the keywords parameter. Defaults to |.
                keyword_all (Boolean): If false, any non-empty subset of the keywords is sufficient to match.
                limit (Integer): The maximum number of studies to return. Defaults to unlimited when missing or negative.
                price_min (Integer): The minimum price, in credits, that a study may have.
                price_max (Integer): The maximum price, in credits, that a study may have.


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
        parser.add_argument("price_min", type=int, default=0)
        parser.add_argument("price_max", type=int, default=-1)

        # the second parameter to each method call is purely for consistency,
        # they don't actually do anything. They should match the defaults above.
        returned_args = parser.parse_args()
        title = returned_args.get("title", None)
        keywords_unsplit = returned_args.get("keywords", None)
        keyword_separator = returned_args.get("keyword_separator", "|")
        keyword_all = returned_args.get("keyword_all", True)
        limit = returned_args.get("limit", -1)
        price_min = returned_args.get("price_min", 0)
        price_max = returned_args.get("price_max", -1)

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
        if price_min <= 0 and price_max < price_min:
            pass
        elif price_min > 0 and price_max < price_min:
            params["CostinCredits"] = {"$gte": price_min}
        elif price_min == price_max:
            params["CostinCredits"] = price_min
        else:
            # price_max is greater than price_min
            # using implicit $and operation
            params["CostinCredits"] = {"$gte": price_min, "$lte": price_max}
        # query database
        studyList = Auxiliary.getStudies(params, limit)
        # convert output
        out = {}
        for i, study in enumerate(studyList):
            out[i] = study.build_dict()
        # return converted output
        return jsonify(out)
