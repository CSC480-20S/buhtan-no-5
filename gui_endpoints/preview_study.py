from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from studystore import FindingFiveStudyStoreStudy
from endpoints import Auxiliary
from endpoints.rating import getReviews


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser(bundle_errors=True)
#studies = [w, x, y, z]


class EndPoint_PreviewStudies(Resource):
    """" Makes the endpoints for GUI to read from
        Args:
             studies (List of FFSS Study) : The study that is being previewed
        Returns:
            Json containing all info about the study except for the template itself
            """

    def get(self):
        built_json = list()
        studies = Auxiliary.getStudies(dict(),4)

        for study in studies:
            study.set_template("na")
            study_dict = study.build_dict()
            study_dict['reviews'] = getReviews(study_dict['studyID'])
            built_json.append(study_dict)
        return jsonify(built_json)


api.add_resource(EndPoint_PreviewStudies, '/studyPreview')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
