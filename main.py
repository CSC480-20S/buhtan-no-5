import os
from flask import Flask, jsonify,send_from_directory
from flask_restful import Resource, Api, reqparse
from Crypto.TokenGenerator import UserToken
from Crypto.PublicTokenGenerator import TokenService
import DbConnection
import FindingFiveStudyStoreUser
import FindingFiveStudyStoreStudy

app = Flask(__name__)
api = Api(app)
# will throw all of the errors at the end
parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('search_param', action='append', required=True, help="The search query")  # user string
parser.add_argument('user_id', type=int, required=True)
parser.add_argument('token', type=int, required=True)
parser.add_argument("credits", type=int, required=True)

class EndPointTesting(Resource):

    def create_user_dict(self, request_args):
        user_dict = dict()
        user_dict["search"] = request_args.get("search_param", None)
        user_dict["user_id"] = request_args.get("user_id", None)
        user_dict["token"] = request_args.get("token", None)
        user_dict["num_of_creds"] = request_args.get("credits", 0)
        return user_dict

    # flask restful allows for each class that inherits from Resource
    # the basic CRUD functions , get delete put update?
    def get(self):
        returned_args = parser.parse_args()
        bla = self.create_user_dict(returned_args)
        return jsonify(bla)


class EndPointDataBase(Resource):
    mini_data = {
        'comment': "An example of study",
        'study_id': 234798239874,
        'rating': 3.2,
        'categories': ['apples', 'bananas', 'order66'],
        'owners': ["jn", "ty", "sheev"],
        'time_created': "YYYY-MM-DD-HR-MM-SS-MC",
        'author': '2398472123097',  # maybe userId?
        "price_in_credits": 69,
        "description": "This could be a long or short message about the study template"
    }

    def get(self):
        return jsonify(self.mini_data)

    def delete(self):
        del self.mini_data['author']
        return '', 200


class ButtonExample(Resource):
    db = {"user_id": 80083, "user_type": 2, "credits": 74}

    def get(self):
        return jsonify(self.db)

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        parser.add_argument("user_type", type=int)
        parser.add_argument("credits", type=int)
        returned_args = parser.parse_args()
        token_gen = UserToken()
        user_created = token_gen.create_token()
        read_vals = token_gen.read_token(user_created)
        self.db["user_id"] = read_vals["user_id"]
        self.db["user_type"] = read_vals["user_type"]
        self.db["credits"] = read_vals["credits"]

class TokenCreation(Resource):
    #maybe should be a post to test the client
    def get(self):
        ts=TokenService()
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        #string representation of ints
        parser.add_argument("user_type", type=str)
        parser.add_argument("credits", type=str)
        parser.add_argument("hash",type=str)
        parser.add_argument("nonce",type=str)
        returned_args = parser.parse_args()
        print(returned_args)
        msg_validty,vals=ts.verify_msg(returned_args)
        # token_generator=UserToken()
        # token = token_generator.create_token()
        # print(type(token))
        # print(token)
        resp = {'valid':msg_validty,"vals":vals,"old":returned_args}
        return jsonify(resp)

def getStudy(study_id):
    """Grabs a study given its ID.

    Pulls from the database and returns a FindingFiveStudyStoreStudy object.

    Args:
        study_id (int): The ID assigned to a study at upload.

    Returns:
        FindingFiveStudyStoreStudy: The associated study in the database.
    """
    #I assume this call returns a dict().
    study = DbConnection.get("studies", study_id)
    return FindingFiveStudyStoreStudy(study["id"], study["title"], study["author"], study["cost"])

def getUser(user_id):
    """Grabs a user given its ID.

        Pulls from the database and returns a FindingFiveStudyStoreUser object.

        Args:
            user_id (String): The ID associated with a user at authentication.

        Returns:
            FindingFiveStudyStoreUser: The associated user in the database.
        """
    #I assume this call returns a dict().
    user = DbConnection.get("users", user_id)
    return FindingFiveStudyStoreUser(user["id"], user["num_credits"], user["owned_studies"], user["viewed_studies"])

def updateUser(user):
    """"Updates a user in the database.

    Pushes a new version of the user data into the database. Assumes the current ID already exists.

    Args:
        user (FindingFiveStudyStoreUser): The new data to write to the database.

    Returns:
        Nothing.
    """
    userDict = {}
    userDict["id"] = user.get_userId()
    userDict["num_credits"] = user.get_numCredits()
    userDict["owned_studies"] = user.get_ownedStudies()
    userDict["viewed_studies"] = user.get_viewedStudies()
    DbConnection.edit("users", userDict["id"], userDict)

class Deliver(Resource):
    def get(self):
        """"Returns the study template.

            Returns the template of the indicated study only if the indicated user owns that study.

            Args:
                user_id (String): The identifier for the user trying to download the template.
                study_id (int): The identifier for the study the user is trying to download.

            Returns:
                JSON: The desired study template, or an error message.
            """
        #obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        parser.add_argument("study_id", type=int)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)
        #verify the parameters exist
        if user_id == None or study_id == None:
            return jsonify({"error":"missing parameter"})
        #get the necessary data from the database
        user = getUser(user_id)
        study = getStudy(study_id)
        #return the study only if owned
        if study_id in user.get_ownedStudies():
            return study.get_template()
        else:
            return jsonify({"error":"user does not own study"})
class Purchase(Resource):
    def get(self):
        """"Establishes an owns relationship between a study and a user.

            Establishes the owns relationship only if the user has sufficient credits and doesn't already own the study.

            Args:
                user_id (String): The identifier for the user trying to purchase the study.
                study_id (int): The identifier for the study the user is trying to purchase.
                credits_available (int): The current credit balance for the user. Overrides any stored balance.

            Returns:
                JSON: The cost of the study, or an error message.
            """
        #obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        parser.add_argument("study_id", type=int)
        parser.add_argument("credits_available", type=int)
        returned_args = parser.parse_args()
        user_id = returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)
        credits_available = returned_args.get("credits_available", None)
        #verify the parameters exist
        if user_id == None or study_id == None or credits_available == None:
            return jsonify({"error": "missing parameter"})
        #get the necessary data from the database
        user = getUser(user_id)
        study = getStudy(study_id)
        cost = study.get_costInCredits()
        #check for sufficient credits and not already owning the study
        if cost > credits_available:
            return jsonify({"error":"insufficient credits"})
        elif study_id in user.get_ownedStudies():
            return jsonify({"error":"user already owns study"})
        #update the user data
        user.set_numCredits(credits_available - cost)
        user.set_ownedStudies(user.get_ownedStudies() + [study_id])
        updateUser(user)
        #return the cost
        return jsonify({"cost":cost})

api.add_resource(EndPointTesting, '/search')
api.add_resource(EndPointDataBase, '/db')
api.add_resource(ButtonExample, '/button')
api.add_resource(TokenCreation, '/tokenCreation')
api.add_resource(Deliver, '/deliver')
api.add_resource(Purchase, '/purchase')


if __name__ == '__main__':
    # runs on localhosts
    app.run(host='0.0.0.0', debug=True)
