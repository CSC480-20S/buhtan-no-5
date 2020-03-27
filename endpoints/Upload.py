from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary
from database import DbConnection
from studystore import FindingFiveStudyStoreStudy

class Upload(Resource):

    @Auxiliary.auth_dec
    def post(self):
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("title", type=str, required=True, help="The study's title.")

        parser.add_argument("author", type=str, required=True,
                            help="Issue with the string reference to the author of the study")
        # we currently have no such thing as a username just an ID, so this is necessarily an ID if its to do anything

        parser.add_argument("costInCredits", type=int, required=True, help="error with Author's price for the study.")
        parser.add_argument("purpose", type=str, required=True, help="missing study's purpose statement.")
        parser.add_argument("references", type=str, action='append', required=True, help="missing references used to"
                                                                                         " design the study.")
        parser.add_argument("categories", type=str, action='append', required=True, help="Issue with"
                                                                                         " study's category(ies).")
        parser.add_argument("subcategories", type=str, action='append', required=True, help="Issue with the study's "
                                                                                            "subcategory(ies).")
        parser.add_argument("keywords", type=str, action='append', required=True, help="Issue with "
                                                                                       "the keywords for the study.")
        parser.add_argument("num_stimuli", type=int, required=True, help="Issue with the number"
                                                                         " of stimuli included in study.")
        parser.add_argument("num_responses", type=int, required=True, help="Issue with the "
                                                                           "number of responses expected from user.")
        parser.add_argument("num_trials", type=int, required=True,
                            help="Issue with the number of trials within a study")
        parser.add_argument("randomize", type=bool, required=True, help="Issue with randomized(question order) param")
        parser.add_argument("duration", type=int, required=True, help="Issue with  expected run time of the study "
                                                                      "from perspective of the surveyed individual")
        parser.add_argument("rating", type=int, help="The study's title.")  # not required presumably
        # todo check this is in fact required v
        parser.add_argument("Institution", type=str, required=True, help="Issue with Institution.")

        # todo template
        parser.add_argument("template", type=str, required=True, help="Missing template")

        returned_args = parser.parse_args()

        constants = DbConnection.connector()["Constants"]
        counter = constants.find_one_and_update({"Next_ID": {"$exists": True}}, {"$inc": {"Next_ID": 1}})
        study_id = counter["Next_ID"]
        title = returned_args.get("title", None)
        author = returned_args.get("author", None)

        costInCredits = returned_args.get("costInCredits", None)
        purpose = returned_args.get("purpose", None)

        # todo: check to ensure that the lists are coming back with proper values
        references = returned_args.get("references", None)
        categories = returned_args.get("categories", None)
        subcategories = returned_args.get("subcategories", None)
        keywords = returned_args.get("keywords", None)
        num_stimuli = returned_args.get("num_stimuli", None)
        num_responses = returned_args.get("num_responses", None)
        num_trials = returned_args.get("num_trials", None)
        randomize = returned_args.get("randomize", None)

        duration = returned_args.get("duration", None)

        rating = returned_args.get("rating", None)
        institution = returned_args.get("institution", None)
        # todo : tepmplate- not sure how to do this at all
        template = returned_args.get("template", None)
        study = FindingFiveStudyStoreStudy(study_id, title, author, costInCredits, purpose, references, categories,
                                           subcategories, keywords, num_stimuli, num_responses, num_trials, randomize,
                                           duration, rating, institution, template)
        connect = DbConnection.connector()["Studies"]
        study_dict = FindingFiveStudyStoreStudy.build_dict(study)
        connect.post("Studies", study_dict)

        # seek = connect.find_one(study, ["Template"])
        # return seek["Template"]

        user = Auxiliary.getUser(author)

        Auxiliary.addOwned(author, study_id, 0)
        # todo : eventually there will be a "Auxilary.addAuthored() method.
        # return ?
