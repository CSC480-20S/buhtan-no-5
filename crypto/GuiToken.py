import jwt
import crypto.PublicTokenGenerator as pg
import datetime
from flask import jsonify
from flask_restful import Resource, reqparse,abort


class Generator(Resource):
    def __init__(self):
        self.key = pg.TokenService.load_secret_key(pg)

    def get(self):
        '''
        This will create a jwt token which is valid for 60 minutes.
        Returns:

        '''
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str, required=True, help="The user ID of the owner is a String.")
        returned_args = parser.parse_args()
        token=self.generate_token(returned_args.get('user_id',None))
        return jsonify({'token':token.decode('UTF-8')})

    def generate_token(self, user_id):
        '''
        Generates the jwt token for access to endpoints.
        This is to simulate F5 providing us with a user token.

        Args:
            user_id(Str): Id of the user requesting a token

        Returns:
            token(dict): Dict representing the token
        '''
        if user_id is None:
              abort(401, description=['UserId must be provided'])
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
            return {'msg': "Invalid token.Please try again.", 'err': e}
        except jwt.DecodeError as e:
            return {'msg': "Error decoding the token. Please try again.", 'err': e}
        except jwt.exceptions.InvalidSignatureError as e:
            return {'msg': "Expired Signature, Please try again", 'err': e}
