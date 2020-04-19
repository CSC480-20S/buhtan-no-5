from flask import jsonify
from flask_restful import Resource, reqparse
from application.endpoints import Auxiliary
from application.database import DbConnection

class GetNotifications(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Returns the list of .notifications sent to a user.

        Returns all notifications sent to a user, starting with the newest.

        Args:
            user_id (String): The identifier for the user for whom the notifications are to be returned.

        Returns:
            JSON: The list of notifications.
        """
        user_id = kwargs["user_id"]
        notifications = getMessages(user_id)
        # return converted output
        return jsonify(notifications)

def getMessages(user_id):
    """"Returns the list of .notifications sent to a user.

    Returns all notifications sent to a user, starting with the newest.

    Args:
        user_id (String): The identifier for the user for whom the notifications are to be returned.

    Returns:
        JSON: The list of notifications.
    """
    # acquire notifications
    connect = DbConnection.connector()["Notifications"]
    seek = connect.find(filter={"User_id": user_id}, sort=[('Timestamp', -1)])
    # build list
    out = []
    for notif in seek:
        out.append({"title": notif["Title"],
                    "body": notif["Body"],
                    "type": notif["Type"],
                    "timestamp": notif["Timestamp"]})
    return out
