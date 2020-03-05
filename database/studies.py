import ssl
from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory
from flask_restful import Resource, Api, reqparse

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


def addViewedStudiesToDB(user_id, study_id):
    """" Get the previewed list from db then modify it by adding a new previewed study with insert and rePost it back to
    database with the updated list.
                    Args:#get the necessary data from the database
                        user_id (String): The identifier for the user trying to purchase the study.
                        study_id (int): The identifier for the study the user is trying to download.
                    Returns:
                        nothing.
"""
    connect = connector()["Users"]
    user = {"User_id": user_id}
    viewStudiesList.insert(0, study_id)
    lister = {"$set": {"Viewed Studies": viewStudiesList}}
    connect.update_one(user, lister)


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


def addOwnedStudiesToDB(user_id, study_id):
    """" Get the owned list from db then modify it by adding a newly bought study with insert and rePost it back to
    database with the updated list.
                    Args:#get the necessary data from the database
                        user_id (String): The identifier for the user trying to purchase the study.
                        study_id (int): The identifier for the study the user is trying to download.
                    Returns:
                        nothing.
"""
    connect = connector()["Users"]
    user = {"User_id": user_id}
    ownedStudiesList.insert(0, study_id)
    lister = {"$set": {"Owned Studies": ownedStudiesList}}
    connect.update_one(user, lister)


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
    addViewedStudiesToDB(1, 1)
    addViewedStudiesToDB(1, 2)
    addViewedStudiesToDB(1, 3)
    addViewedStudiesToDB(1, 4)
    addViewedStudiesToDB(1, 5)
    addViewedStudiesToDB(1, 6)
    addViewedStudiesToDB(1, 7)
    addViewedStudiesToDB(1, 8)
    addViewedStudiesToDB(1, 9)
    addViewedStudiesToDB(1, 10)
    addOwnedStudiesToDB(1, "tommy")
    addOwnedStudiesToDB(1, "johnB")
    addOwnedStudiesToDB(1, "shaunG")
    addOwnedStudiesToDB(1, "benG")
    addOwnedStudiesToDB(1, "AnnaS")
    addOwnedStudiesToDB(1, "ethanM")
    addOwnedStudiesToDB(1, "Adrian.")
    # runs on local hosts
    app.run(host='0.0.0.0', debug=True)
