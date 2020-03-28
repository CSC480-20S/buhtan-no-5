from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary


class Search(Resource):
    @Auxiliary.auth_dec
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
            If duration_min is given, return only studies at that duration or higher.
            If duration_max is given, return only studies at that duration or lower.
            If duration_min is greater than duration_max, ignore duration_max.
            For the purposes of this method, the duration of a study may not be negative,
            so all negative values of duration_min and duration_max will be ignored.
            If rating_min is given, return only studies with that rating or higher.
            If rating_max is given, return only studies with that rating or lower.
            If rating_min is greater than or equal to rating_max, ignore rating_max.
            The valid options for rating_min and rating_max are 0, 1, 2, 3, 4, and 5.
            If rating_min and/or rating_max are given and include_unrated is false, return only studies with at least one review.
            If include_unrated is true or omitted, all unrated studies will be considered part of whatever rating range was specified.
            If none of the three rating parameters are given, the rating data will be ignored.
            If category is given, return only studies with that category.
            ...in progress.

            Args:
                title (String): The title that a study must have..
                keywords (String): Contains all the keywords that a study must have.
                keyword_separator (String): Separates the keywords in the keywords parameter. Defaults to |.
                keyword_all (Boolean): If false, any non-empty subset of the keywords is sufficient to match.
                limit (Integer): The maximum number of studies to return. Defaults to unlimited when missing or negative.
                price_min (Integer): The minimum price, in credits, that a study may have.
                price_max (Integer): The maximum price, in credits, that a study may have.
                duration_min (Integer): The minimum duration, in minutes, that a study may have.
                duration_max (Integer): The maximum duration, in minutes, that a study may have.
                rating_min (Integer): The minimum rating that a study may have. Must be in the range [0, 5].
                rating_max (Integer): The maximum rating that a study may have. Must be in the range [0, 5].
                include_unrated (Boolean): If false, unrated studies will not be returned.
                category (String): The category that a study must have.


            Returns:
                JSON: The list of studies that meet the specified requirements.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("title", type=str)
        parser.add_argument("keywords", type=str)
        parser.add_argument("keyword_separator", type=str, default="|")
        parser.add_argument("keyword_all", type=inputs.boolean, default=True)
        parser.add_argument("limit", type=int, default=-1)
        parser.add_argument("price_min", type=int, default=0)
        parser.add_argument("price_max", type=int, default=-1)
        parser.add_argument("duration_min", type=int, default=0)
        parser.add_argument("duration_max", type=int, default=-1)
        parser.add_argument("rating_min", type=int, default=0, options=(0, 1, 2, 3, 4, 5))
        parser.add_argument("rating_max", type=int, default=5, options=(0, 1, 2, 3, 4, 5))
        parser.add_argument("include_unrated", type=inputs.boolean, default=True)
        parser.add_argument("category", type=str)

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
        duration_min = returned_args.get("duration_min", 0)
        duration_max = returned_args.get("duration_max", -1)
        rating_min = returned_args.get("rating_min", 0)
        rating_max = returned_args.get("rating_max", 5)
        include_unrated = returned_args.get("include_unrated", True)
        category = returned_args.get("category", None)

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
        if duration_min <= 0 and duration_max < 0:
            pass
        elif duration_min > 0 and duration_max < duration_min:
            params["Duration"] = {"$gte": duration_min}
        elif duration_min == duration_max:
            params["Duration"] = duration_min
        elif duration_min < 0 and duration_max >= 0:
            params["Duration"] = {"$lte": duration_max}
        else:
            # duration_max is greater than duration_min
            # using implicit $and operation
            params["Duration"] = {"$gte": duration_min, "$lte": duration_max}
        if include_unrated:
            pass
        else:
            params["Number of Reviews"] = {"$gt": 0}
        if rating_min == 0 and rating_max == 5:
            pass
        elif rating_min >= rating_max or rating_max == 5:
            params["$expr"] = {"%gte": ["$Total Stars", {"$multiply": ["$Number of Reviews", rating_min]}]}
        elif rating_min == 0:
            params["$expr"] = {"%lte": ["$Total Stars", {"$multiply": ["$Number of Reviews", rating_max]}]}
        else:
            # sub range without a default endpoint
            params["$expr"] = {"%gte": ["$Total Stars", {"$multiply": ["$Number of Reviews", rating_min]}],
                               "%lte": ["$Total Stars", {"$multiply": ["$Number of Reviews", rating_max]}]}
        if category is not None:
            # using $in so that we can make Categories an array or string without breaking this code
            params["Categories"] = {"$in": [category]}
        # query database
        studyList = Auxiliary.getStudies(params, limit)
        # convert output
        out = {}
        for i, study in enumerate(studyList):
            out[i] = study.build_dict()
        # return converted output
        return jsonify(out)
