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