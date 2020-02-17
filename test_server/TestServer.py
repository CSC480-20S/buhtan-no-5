import requests as req
from flask import Flask, jsonify,json
from flask_restful import Resource, Api
from TokenGenerator import UserToken


app = Flask(__name__)
api = Api(app)

class ClientServer(Resource):

    dummy_user= {"user_id":000,"user_type":0,"credits":20}



    def get(self):
        #to test the client getting the token
        response=req.get("http://localhost:5000/tokenCreation")
        print(response.content)
        user_token=json.loads(response.text)
        print(type(user_token))
        decoded_token=UserToken().read_token(user_token)
        return jsonify(decoded_token)





api.add_resource(ClientServer,'/simulate')

if __name__ == '__main__':
    # runs on localhosts
    app.run(host='0.0.0.0', debug=True,port="6868")
