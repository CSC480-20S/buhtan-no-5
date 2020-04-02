from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from endpoints import Auxiliary
from database import DbConnection

class GetImage(Resource):

    @Auxiliary.auth_dec
    def get(self):
        """Returns an image from the database.

        Returns the image specified by image_id in base64 format.

        Args:
            image_id (String): The image ID of the image to be returned.


        Returns:
            JSON: {"base64": image}, where image is the base64 encoding of the requested image.
        """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("image_id", type=str, required=True, help="Image ID is a string.")

        returned_args = parser.parse_args()
        image_id = returned_args.get("image_id", None)

        image = {"Image_id": image_id}
        connect = DbConnection.connector()["Images"]
        seek = connect.find_one(image)

        return jsonify({"base64": seek["Base64"]})
