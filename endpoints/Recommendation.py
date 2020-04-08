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
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str, required=True,
                            help="The user_id is string representation of user's ID.")
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        user = Auxiliary.getUser(user_id)
        pref_study_ids = set(
            user.get_ownedStudies() + user.get_viewedStudies() + user.get_wishList() + user.get_authorList())
        studies = [study for id in pref_study_ids if (study := Auxiliary.getOptionalStudy(id))]
        # categories = [cat for study in studies if(cat := study.get_categories())]
        # subcategories = [sub for study in studies if()]
        categorical_key_terms = []

        functions = [Study.get_categories, Study.get_subcategories, Study.get_keywords]
        cats, subcats, keywordz = [flatten(x for study in studies if (x := remove_nones(f(study)))) for f in functions]
        # print(cats)
        # print(subcats)
        # print(keywordz)

        duplicate_cats, duplicate_subcats, duplicate_keywordz = \
            [[term for term, count in Counter(c).items() if count > 1]
             for c in [cats, subcats, keywordz]]

        params = {}
        if duplicate_cats:
            params["Categories"] = {"$in": duplicate_cats}
        elif cats:
            params["Categories"] = {"$in": cats}

        if duplicate_subcats:
            params["Sub_Categories"] = {"$in": duplicate_subcats}
        elif subcats:
            params["Sub_Categories"] = {"$in": subcats}

        if duplicate_keywordz:
            params["Keywords"] = {"$in": duplicate_keywordz}
        elif keywordz:
            params["Keywords"] = {"$in": keywordz}

        print(list(set(Auxiliary.getStudies(params, 75))))

        studylist = list(set(Auxiliary.getStudies(params, 75)))

        studylist.sort(key=lambda study: study.get_rating(), reverse=True)

        return jsonify(Auxiliary.studyListToDictList(studylist))

        print([x["rating"] for x in Auxiliary.studyListToDictList(studylist)])
        # print(len(studylist))



        '''
        cats = []
        subcats = []
        keywordz = []

        for study in studies:
            if (temp := study.get_categories()) and (temp2 := study.get_subcategories()) and (
                    temp3 := study.get_keywords()):
                cats += temp
                subcats += temp2
                keywordz += temp3
                
        '''

        # print(categorical_key_terms)
        # print(list(dict.fromkeys(categorical_key_terms)))
        # print([term for term, count in collections.Counter(categorical_key_terms).items() if count > 1]) # repeated categorical keywords
        # print(cats)
        # print(subcats)

        # repeated_cats = [term for term, count in collections.Counter(keywordz).items() if count > 1]
        # repeated_subcats = [term for term, count in collections.Counter(subcats).items() if count > 1]
        # repeated_keywords = [term for term, count in collections.Counter(keywordz).items() if count > 1]


def flatten(list):
    return [y for x in list for y in x]


def remove_nones(list):
    return [x for x in list if x]
