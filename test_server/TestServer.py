import requests as req
from flask import Flask, jsonify,json
from flask_restful import Resource, Api
from Crypto.TokenGenerator import UserToken
import hashlib as hl
import binascii

app = Flask(__name__)
api = Api(app)

class ClientServer(Resource):

    dummy_user= {"user_id":'kazookid',"user_type":2,"credits":20}



    def get(self):
        #to test the client getting the token
        url="http://localhost:5000/tokenCreation"
        dummy_hash = hl.sha256()
        dummy_hash.update(binascii.hexlify(str(self.dummy_user["user_id"]+str(self.dummy_user["user_type"])+str(self.dummy_user["credits"])).encode("utf-8")))
        print(type(dummy_hash.hexdigest()))
        self.dummy_user["hash"]=dummy_hash.hexdigest()
        data=self.dummy_user
        response=req.get(url,json=data)
        return response.json()
        # user_token=json.loads(response.text)
        # print(type(user_token))
        # decoded_token=UserToken().read_token(user_token)
        #return jsonify(decoded_token)





api.add_resource(ClientServer,'/simulate')

if __name__ == '__main__':
    # runs on localhosts
    app.run(host='0.0.0.0', debug=True,port="6868")
