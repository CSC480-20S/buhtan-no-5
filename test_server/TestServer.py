import binascii
import hashlib as hl
import os
import requests as req
from nacl import secret, utils,encoding
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class ClientServer(Resource):
    dummy_user = {"user_id": 'kazookid', "user_type": 2, "credits": 20}

    def __init__(self):
        self.secret_key = self.load_secret_key()

    def encrypt_fields(self):
        print(self.secret_key)
        box=secret.SecretBox(self.secret_key)
        self.dummy_user["user_id"]=box.encrypt((self.dummy_user["user_id"]).encode('utf-8'))
        self.dummy_user["user_type"]=box.encrypt(self.dummy_user["user_type"])
        self.dummy_user["credits"]=box.encrypt(self.dummy_user["credits"])
        print(type(self.dummy_user["credits"]))


    def load_secret_key(self):
        load_dotenv('secrets.env')
        secret_key = os.getenv('secret_key')
        if secret_key is None:
            server_key = self.create_keys()
            return server_key
        return secret_key


    def create_keys(self):
    # create the server key  and stores in a local file.
        server_key = utils.random(secret.SecretBox.KEY_SIZE)
        with open("Private.env", "wb") as f:
            f.write(server_key)
        return server_key

    def get(self):
        # to test the client getting the token
        url = "http://localhost:5000/tokenCreation"
        dummy_hash = hl.sha256()
        self.encrypt_fields()
        print(self.dummy_user["user_id"])
        dummy_hash.update(binascii.hexlify(self.dummy_user["user_id"] + self.dummy_user["user_type"] + self.dummy_user["credits"]))
        print(dummy_hash.hexdigest())
        self.dummy_user["hash"] = dummy_hash.hexdigest()
        data = self.dummy_user
        response = req.get(url, json=data)
        return response.json()


api.add_resource(ClientServer, '/simulate')

if __name__ == '__main__':
    # runs on localhosts
    app.run(host='0.0.0.0', debug=True, port="6868")
