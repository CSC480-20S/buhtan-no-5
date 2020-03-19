import jwt
import crypto.PublicTokenGenerator as pg
import datetime
from flask_restful import Resource, reqparse


class Generator():
    def __init__(self):
        self.key = pg.TokenService.load_secret_key(pg)

    def generate_token(self, user_id):
        '''
        Generates the jwt token for access to endpoints.

        Args:
            user_id(Str): Id of the user requesting a token

        Returns:
            token(dict): Dict representing the token
        '''

        try:
            utc = datetime.datetime.utcnow()

            resp = {'iat': utc,
                    'exp': (utc + datetime.timedelta(minutes=60)),
                    'sub': user_id,
                    }

            return jwt.encode(resp, self.key, algorithm='HS256')
        except TypeError as te:
            return 400

    def authenticate_token(self, alleged_token):
        '''
        Authenticate the provide token.
        Args:
            alleged_token(dict):Represents the token passed by the user.

        Returns:
            user_id(Str): the user_id in the provided token
        '''
        try:
            payload = jwt.decode(alleged_token, self.key)
            return payload['sub']
        except jwt.InvalidTokenError as e:
            return {'msg':"Invalid token.Please try again.",'err':e}
        except jwt.DecodeError as e:
            return {'msg':"Error decoding the token. Please try again.",'err':e}
        except jwt.exceptions.InvalidSignatureError as e:
            return {'msg':"Expired Signature, Please try again",'err':e}
