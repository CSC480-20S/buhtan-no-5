from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study

def getStudy(study_id):
    """Grabs a study given its ID.

    Pulls from the database and returns a FindingFiveStudyStoreStudy object.

    Args:
        study_id (int): The ID assigned to a study at upload.

    Returns:
        FindingFiveStudyStoreStudy: The associated study in the database.
    """

    connect = DbConnection.connector()["Studies"]
    study = {"Study_id": study_id}
    seek = connect.find_one(study)
    return f5study(study_id, seek["Title"], seek["Author"], seek["CostinCredits"], seek["Purpose"], seek["References"],
                   seek["Categories"], seek["Sub_Categories"], seek["Keywords"], seek["Num_Stimuli"],
                   seek["Num_Responses"], seek["Randomize"], seek["Duration"], seek["Num_trials"], seek["Rating"],
                   seek["Institution"], seek["Template"])

def getUser(self,user_id):
    """Grabs a user given its ID.

    Pulls from the database and returns a FindingFiveStudyStoreUser object.

    Args:
        user_id (String): The ID associated with a user at authentication.

    Returns:
        FindingFiveStudyStoreUser: The associated user in the database.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id}
    seek = connect.find_one(user)
    return f5user(user_id, seek["Num Credits"], seek["Owned Studies"], seek["Viewed Studies"])

def updateUser(user):
    """"Updates a user in the database.

    Pushes a new version of the user data into the database. Assumes the current ID already exists.

    Args:
        user (FindingFiveStudyStoreUser): The new data to write to the database.

    Returns:
        Nothing.
    """

    connect = DbConnection.connector()["Users"]
    userJ = {"User_id": user.get_userId()}
    changes = {"$set":{"Num Credits": user.get_numCredits(),
                       "Owned Studies": user.get_ownedStudies(),
                       "Viewed Studies": user.get_viewedStudies()}}
    connect.update_one(userJ, changes)
