from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from endpoints import transaction_blueprint as tbp
from crypto import crypto_blueprint as cbp
from deployment import deployment_blueprint as dbp
from exceptions import Authentication as auth

def create_app():
    app = Flask(__name__,instance_relative_config=False)


    with app.app_context():
        app.register_blueprint(tbp.trans_bp)
        app.register_blueprint(cbp.crypto_bp)
        app.register_blueprint(dbp.deployment_bp)
        app.register_error_handler(401, auth.handle_auth)
        app.register_error_handler(501,auth.malformed_url_query)
        app.register_error_handler(500,auth.generic_exception)
        CORS(app)
        Api(app)
