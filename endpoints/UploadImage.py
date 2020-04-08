from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from endpoints import Auxiliary
from database import DbConnection

class UploadImage(Resource):

    @Auxiliary.auth_dec
    def post(self,**kwargs):
        """Uploads a new image to the database.

        Uploaded images are assigned a String ID, which is returned.
        It is expected that the returned ID will be stored with the referencing study.
        The user ID of the uploader is stored for ddtabase review purposes.
        A timestamp is also stored.

        Args:
            user_id (String): The user ID of the user uploading the image.
            base64 (String): The image in base64 format.


        Returns:
            JSON: {"image_id": id}, where id is the generated String id.
        """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        #parser.add_argument("user_id", type=str, required=True, help="User ID is a string.")
        parser.add_argument("base64", type=str, required=True,
                            help="An image String in base64 encoding.")

        returned_args = parser.parse_args()
        user_id = kwargs["user_id"]  #returned_args.get("user_id", None)
        base64 = returned_args.get("base64", None)

        connection = DbConnection.connector()
        constants = connection["Constants"]
        counter = constants.find_one_and_update({"Next_Image_ID": {"$exists": True}}, {"$inc": {"Next_Image_ID": 1}})
        image_id = str(counter["Next_Image_ID"])

        image_dict = {"User_id": user_id, "Image_id": image_id, "$currentDate": {"Upload Date": {"$type": "timestamp"}}, "Base64": base64}

        connection["Images"].insert(image_dict)

        return jsonify({"image_id": image_id})
