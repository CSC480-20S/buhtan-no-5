from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from studystore import FindingFiveStudyStoreStudy
import json

x = FindingFiveStudyStoreStudy.FindingFiveStudyStoreStudy(42, "hell0 world", "John Bald", 50, "the purpose of this is to show that we can do fun things", "references are not fun", "HCI", "usability", ["keyword1", "keyword2"], 10, 14, True, "15 minutes", 21, 5, "SUNY Oswego", "template1")
y = FindingFiveStudyStoreStudy.FindingFiveStudyStoreStudy(42, "hell1 world", "Tom", 51, "the purpose of this is to show that we can do fun things too", "references are not fun here either", "Social", "subcat", ["keyword3", "keyword4"], 11, 15, False, "10 minutes", 22, 2, "SUNY Oswego", "template2")
w = FindingFiveStudyStoreStudy.FindingFiveStudyStoreStudy(123456, "mystudies", "Nahyro", 123456, "to test", "my Dreams","ISC", "science", ["key1", "key2", "key3"], 4, 5, True, "30 minutes", 3, 3, "Oswego", "template3")
z = FindingFiveStudyStoreStudy.FindingFiveStudyStoreStudy(999999, "bop", "Tommy", 42, "this is a bop", "pls love me", "CSC", "science rulez", ["kw1", "kw2", "kw3"], 2, 15, True, "20 minutes", 4, 5, "Webster", "Rubber Duck")

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser(bundle_errors=True)
studies = [w, x, y, z]

class EndPoint_PreviewStudies(Resource):
    """" Makes the endpoints for GUI to read from
        Args:
             studies (List of FFSS Study) : The study that is being previewed
        Returns:
            Json containing all info about the study except for the template itself
            """

    def post(self):
        built_json = list()
        for study in studies:
            study.set_template("na")
            built_json.append(study.build_dict())
        return jsonify(built_json)



api.add_resource(EndPoint_PreviewStudies, '/studyPreview')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug =True )