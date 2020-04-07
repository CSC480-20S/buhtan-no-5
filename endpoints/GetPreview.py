from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary


class GetPreview(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Provides the full details for a study from the database to a user.

            Provides a study, in JSON format, with all fields of data except the template, given the ID of the study.
            Also adds the study to the user's preview history, even if already present.
            Intended for use in normal previewing.
            For administrative review, use GetAdminDetails.get().

            Args:
                study_id (Integer): The identifier of the study to be reviewed.
                user_id (String): The indentifier of the user previewing the study.


            Returns:
                JSON: The study without its template.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("study_id", type=int, required=True, help="Specify a study for details.")
        parser.add_argument("user_id", type=str, required=True, help="Specify which user is previewing the study.")

        # the second parameter to each method call is purely for consistency,
        # they don't actually do anything. They should match the defaults above.
        returned_args = parser.parse_args()
        study_id = returned_args.get("study_id", None)
        user_id = returned_args.get("user_id", None)

        # query database
        study = Auxiliary.getStudy(study_id)
        study.set_template("Template redacted")

        # add the study to the user's preview list
        Auxiliary.addViewed(user_id, study_id)

        # return converted output
        return jsonify(study.build_dict())
