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

def getStudies(params, maxStudies=-1):
    """Grabs a list of studies given some parameters they need to meet.

    Pulls from the database and returns a list of FindingFiveStudyStoreStudy objects.
    Each object will have the fields given in params equal to the values paired with them in params.

    Args:
        params (dict): Pairs field names with the values they must have.
        maxStudies (int): If greater than or equal to zero, no more than max studies will be in the output list.

    Returns:
        list<FindingFiveStudyStoreStudy>: The first "max" studies that have the given params.
    """

    #if asked for zero studies, just return
    if (maxStudies == 0):
        return []
    #change to the number the Mongo code likes uses for no limit
    elif (maxStudies < 0):
        maxStudies = 0

    #acquire studies
    connect = DbConnection.connector()["Studies"]
    seek = connect.find(filter=params, projection={"Template":False}, limit=maxStudies)

    #get the number of studies returned - {} gives us all
    numStudies = seek.collection.count_documents({})

    studyList = []
    #not sure if this actually returns a list
    for study in seek[0:numStudies]:
        studyList.append(f5study(study["Study_id"], study["Title"], study["Author"], study["CostinCredits"], study["Purpose"], study["References"],
                study["Categories"], study["Sub_Categories"], study["Keywords"], study["Num_Stimuli"],
                study["Num_Responses"], study["Randomize"], study["Duration"], study["Num_trials"], study["Rating"],
                study["Institution"], "Template redacted"))
    return studyList

def getUser(user_id):
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

def addOwned(user_id, study_id, cost):
    """Decreases a user's credits to purchase a study.

    Atomically decreases a user's credits and adds the study to the user's list of owned studies.
    Does not verify that the referenced study actually exists.
    If the study is already in the list, a duplicate will not be created.

    Args:
        user_id (String): The ID of the user purchasing the study.
        study_id (Integer): The ID of the study being purchased.
        cost (Integer): The positive number of credits to deduct from the user for the study.

    Returns:
        Nothing.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id":user_id}
    changes = {"$inc":{"Num Credits":0-cost},
               "$addToSet":{"Owned Studies":study_id}}
    connect.update_one(user, changes)