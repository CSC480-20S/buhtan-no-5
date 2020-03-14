import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from crypto.TokenGenerator import UserToken
from crypto.PublicTokenGenerator import TokenService
from endpoints import transaction_blueprint as tbp

app = Flask(__name__)
app.register_blueprint(tbp.trans_bp)
CORS(app)
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

api.add_resource(EndPointTesting, '/search')
api.add_resource(EndPointDataBase, '/db')
api.add_resource(ButtonExample, '/button')
api.add_resource(TokenCreation, '/tokenCreation')

if __name__ == '__main__':
    # runs on localhosts
    app.run(host='129.3.20.26', port=12100 debug=True)
