import ssl
from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory
from flask_restful import Resource, Api, reqparse
from endpoints import Auxiliary

app = Flask(__name__)
api = Api(app)
# will throw all of the errors at the end
parser = reqparse.RequestParser(bundle_errors=True)
viewStudiesList = []
ownedStudiesList = []


def connector():
    client = MongoClient(
        "mongodb+srv://Engine:qhcFrP65n8joJvso@cluster0-v76zg.mongodb.net/test?retryWrites=true&w=majority", ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE)
    db = client["StudyStore"]
    return db


def processor(idea):
    connect = connector()["Studies"]
    study = {"Study_id": idea}
    info = connect.find_one(study)
    print(info)
    return info





# Viewing the previously viewed studies
class EndPointViewedStudies(Resource):
    """" Pulls the previewed studies for the database.
                Args:
                    user_id (String): The identifier for the user who viewed the studies.
                Returns:
                    JSON: The list of previewed studies.
                """
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        print(returned_args)
        connect = connector()["Users"]
        # need to fix this get functions
        user = {"User_id": 1}
        seek = connect.find_one(user)
        search = seek["Viewed Studies"]
        print("previewed studies are:", search[0:4])
        preview = {'Previewed Studies': search[0:4]}
        return jsonify(preview)



# Viewing the owned studies
class EndPointOwnedStudies(Resource):
    """" Pulls the owned studies for the database.
                Args:
                    user_id (String): The identifier for the user who owns the studies.
                Returns:
                    JSON: The list of owned studies.
                """
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        # print(returned_args)
        connect = connector()["Users"]
        # need to fix this get functions
        user = {"User_id": 1}
        seek = connect.find_one(user)
        search = seek["Owned Studies"]
        print("search is: ", search)
        preview = {'Owned Studies': search}
        return jsonify(preview)


api.add_resource(EndPointViewedStudies, '/previewed')
api.add_resource(EndPointOwnedStudies, '/Owned')

if __name__ == '__main__':
    Auxiliary.addViewed("1", 1)
    Auxiliary.addViewed("1", 2)
    Auxiliary.addViewed("1", 3)
    Auxiliary.addViewed("1", 4)
    Auxiliary.addViewed("1", 5)
    Auxiliary.addViewed("1", 6)
    Auxiliary.addViewed("1", 7)
    Auxiliary.addViewed("1", 8)
    Auxiliary.addViewed("1", 9)
    Auxiliary.addViewed("1", 10)
    Auxiliary.addOwned("1", 0, 0)
    Auxiliary.addOwned("1", 1, 0)
    Auxiliary.addOwned("1", 2, 0)
    Auxiliary.addOwned("1", 3, 0)
    Auxiliary.addOwned("1", 4, 0)
    Auxiliary.addOwned("1", 5, 0)
    Auxiliary.addOwned("1", 6, 0)
    # runs on local hosts
    app.run(host='0.0.0.0', debug=True)
