from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from studystore import FindingFiveStudyStoreStudy
from endpoints import Auxiliary


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
        studies = Auxiliary.getStudies(dict(),4) #list()

        for study in studies:
            study.set_template("na")
            built_json.append(study.build_dict())
        return jsonify(built_json)


api.add_resource(EndPoint_PreviewStudies, '/studyPreview')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
