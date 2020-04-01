from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from endpoints import Auxiliary
from database import DbConnection
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy

class Upload(Resource):

    @Auxiliary.auth_dec
    def post(self):
        """Uploads a new study to the database.

        Uploaded studies are not visible in the store's search results until they are approved by an administrator.
        Adds the new study to the author's author list and owned list.
        Note the difference between author and author_id:
        author is intended to be displayed to other users,
        while author_id is used for internal referencing.
        They can be the same, but security may be improved by not displaying other user's IDs.

        Args:
            title (String): The title of the study.
            author (String): The author of the study, as it should be displayed.
            costInCredits (Integer): The cost of the study in credits. Negative values are possible, but will not be
                                     returned when filtering by price.
            purpose (String): The purpose of the study.
            references (String): The reference that others should use when referencing this study.
            categories (List of Strings): The main categories that the study belongs to.
            subcategories (List of Strings): The subcategories that the study belongs to.
            keywords (List of Strings): The keywords associated with a study.
            num_stimuli (Integer): The number of stimuli that the study uses.
            num_responses (Integer): The number of responses that the study uses.
            num_trials (Integer): The number of trials that the study uses.
            randomize (Boolean): Whether the study uses randomization.
            duration (Integer): The expected duration, in minutes, of the study.
            institution (String): The institution associated with the author or study.
            template (String): The JSON study template from FindingFive.
            images (List of Strings): The images for display when previewing the study.
                                      May be references to external images, or may be base64 encoded images.
            abstract (String): The abstract of the study. Acts as a description.
            author_id (String): The user ID of the author.


        Returns:
            JSON: {"Success": True} if the study successfully uploaded.
        """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("title", type=str, required=True, help="Title should be string.")
        parser.add_argument("author", type=str, required=True,
                            help="Issue author should be String")
        parser.add_argument("costInCredits", type=int, required=True, help="Issue with cost . should be int")
        parser.add_argument("purpose", type=str, required=True, help="missing study's purpose statement, string")
        parser.add_argument("references", type=str, required=True, help="missing references used to"
                                                                                         " design the study, string")
        parser.add_argument("categories", type=str, action='append', required=True, help="Issue with"
                                                                                         " study's category, string")
        parser.add_argument("subcategories", type=str, action='append', required=True, help="Issue with the study's "
                                                                                            "subcategory, string")
        parser.add_argument("keywords", type=str, action='append', required=True, help="Issue with "
                                                                                       "the keywords, string")
        parser.add_argument("num_stimuli", type=int, required=True, help="Issue with the number"
                                                                         " of stimuli included in study, int")
        parser.add_argument("num_responses", type=int, required=True, help="Issue with the "
                                                                           "number of responses expected from user, int")
        parser.add_argument("num_trials", type=int, required=True,
                            help="Issue with the number of trials within a study, int")
        parser.add_argument("randomize", type=inputs.boolean, required=True, help="Issue with randomized(question order) "
                                                                        "param,bool")
        parser.add_argument("duration", type=int, required=True, help="Issue with  expected run time of the study "
                                                                      "from perspective of the surveyed individual, int")
        parser.add_argument("institution", type=str, required=True, help="Issue with institution, string")
        parser.add_argument("template", type=str, required=True, help="Issue with / Missing template, string")
        parser.add_argument("images", type=str, action="append", required=True, help="Images are stored/referenced with Strings.")
        parser.add_argument("abstract", type=str, required=True, help="Abstract is a description String.")
        parser.add_argument("author_id", type=str, required=True, help="The author_id is the user_id of the uploading user.")

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
        template = returned_args.get("template", None)
        images = returned_args.get("images", None)
        abstract = returned_args.get("abstract", None)
        author_id = returned_args.get("author_id", None)
        study = FindingFiveStudyStoreStudy(study_id, title, author, costInCredits, purpose, references, categories,
                                           subcategories, keywords, num_stimuli, num_responses, randomize,
                                           duration, num_trials, rating, institution, template, images, abstract, author_id)
        # connect = DbConnection.connector()["Studies"]
        study_dict = study.build_database_doc()
        # connect.insert_one("Studies", study_dict).inserted_id

        DbConnection.connector()["Studies"].insert(study_dict)

        # seek = connect.find_one(study, ["Template"])
        # return seek["Template"]

        # user = Auxiliary.getUser(author)

        # Auxiliary.addOwned(user, study_id, 1)
        # todo : eventually there will be a "Auxiliary.addAuthored() method.
        return "work pls"
