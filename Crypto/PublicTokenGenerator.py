import binascii
import hashlib as hl
from nacl import secret, utils
from dotenv import load_dotenv
import os


class TokenService():
    def __init__(self):
        self.secret_key = self.load_secret_key()

    def load_secret_key(self):
        load_dotenv('secrets.env')
        secret_key = os.getenv('secret_key')
        if secret_key is None:
            server_key = self.create_keys()
            return server_key
        return secret_key

    def decrypt(self, client_resp):
        box = secret.SecretBox(self.secret_key)
        print(box.decrypt(client_resp['user_id']))
        print(box.decrypt(client_resp["user_type"]))
        print(box.decrypt(client_resp["credits"]))
    # print(box.decrypt())


def verify_msg(self, client_resp):
    user_id = client_resp['user_id']
    user_type = client_resp["user_type"]
    credits = client_resp["credits"]
    user_hash = client_resp["hash"]
    hashy = hl.sha256()
    user_hex_vals = binascii.hexlify(str(str(user_id) + str(user_type) + str(credits)).encode("utf-8"))
    hashy.update(user_hex_vals)
    print(hashy.hexdigest())
    print(user_hash)
    if hashy.hexdigest() == user_hash:
        return True
    return False


def create_keys(self):
    # create the server key  and stores in a local file.
    server_key = utils.random(secret.SecretBox.KEY_SIZE)
    with open("Private.env", "wb") as f:
        f.write(server_key)
    return server_key
# updated token
# client_token={"user_id":0,"user_type":0,"credits":0,"hash":0}
