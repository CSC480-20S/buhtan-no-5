from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary


class GetPending(Resource):
    @Auxiliary.auth_dec
    def get(self):
        """"Provides a list of pending studies from the database.

            Provides a list of studies, in JSON format, that have been neither approved nor denied.
            If limit is given, no more than limit studies will be returned.

            Args:
                limit (Integer): The maximum number of studies to return. Defaults to unlimited when missing or negative.


            Returns:
                JSON: The list of pending studies.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("limit", type=int, default=-1)

        # the second parameter to each method call is purely for consistency,
        # they don't actually do anything. They should match the defaults above.
        returned_args = parser.parse_args()
        limit = returned_args.get("limit", -1)

        # build search parameters
        params = {"Status": "Waiting for review"}

        # query database
        studyList = Auxiliary.getStudies(params, limit)
        # convert output
        out = Auxiliary.studyListToDictList(studyList)
        # return converted output
        return jsonify(out)