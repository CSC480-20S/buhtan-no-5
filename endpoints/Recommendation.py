from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from endpoints import Auxiliary
from database import studies as db_studies
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as Study
import collections
from collections import Counter


class Recommendation(Resource):

    @Auxiliary.auth_dec
    def get(self, **kwargs):
        """Suggest studies for user.

            Pull historic user interaction data from DB, given user_id, and generate reccomended list of studies
            based on key phrases. Prioritized by rating

            Args:
                user_id (int): The ID assigned to a user.

            Returns:
                FindingFiveStudyStoreStudy list: ordered list of studies recommended to user, highest rated to lowest
            """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str, required=True,
                            help="The user_id is string representation of user's ID.")
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        user = Auxiliary.getUser(user_id)
        pref_study_ids = set(
            user.get_ownedStudies() + user.get_viewedStudies() + user.get_wishList() + user.get_authorList())


        studies = []
        for id in pref_study_ids:
            study = Auxiliary.getOptionalStudy(id)
            if study:
                studies.append(study)

        if not studies:
            return {"error": "you don't have any study interactions, usez our site to GET recommendations!"}
        params = {}

        def valid_study(study):
            return study.get_authorID() != user_id

        def add_param(function, param_name):
            values = []
            for study in studies:
                list_no_nones = remove_nones(function(study))
                if (list_no_nones):
                    values.append(list_no_nones)
            values = flatten(values)

            duplicates = [e for e, count in Counter(values).items() if count > 1]

            if duplicates:
                params[param_name] = {"$in": duplicates}
            elif values:
                params[param_name] = {"$in": values}

        add_param(Study.get_categories, "Categories")
        add_param(Study.get_subcategories, "Sub_Categories")
        add_param(Study.get_keywords, "Keywords")

        full_study_list = list(set(Auxiliary.getStudies(params, 75)))
        filtered_study_list = list(filter(valid_study, full_study_list))

        study_list = filtered_study_list if filtered_study_list else full_study_list
        study_list.sort(key=lambda study: study.get_rating(), reverse=True)

        return jsonify(Auxiliary.studyListToDictList(study_list))


def flatten(list):
    return [y for x in list for y in x]


def remove_nones(list):
    return [x for x in list if x]
