from database import DbConnection
def ratingsys(id, user, rate, comment):
    # id is the Study_id of the study to be rated along with rate being the rate being processed
    ratelist = []
    connect = DbConnection.connector()
    review = connect["Reviews"]
    rater = connect["Studies"]
    query = review.find({"Study_id": id})
    for rates in query:
        ratelist.append(rates["Rating"])
    ratelist.append(rate) # adds the new rating to the list of ratings of this study
    average = sum(ratelist) / len(ratelist)  # Gets the average rating of this study
    average = round(average)  # this average is then converted to a whole number
    rater.update_one({ "Study_id": id}, {"$set": {"Rating": average}})
    # The new rate of the study along with new list of ratings is then updated to mongodb database
    review.insert_one({"Study_id": id, "User_id": user, "Rating": rate, "Comment": comment})
    # this review is now stored

def getReviews(study_id):
    """Returns all the reviews for a given study.

    Each review is limited to the name, occupation, rating, and comment.

    Args:
        study_id (Integer): The identifier of the study for which to return reviews.

    Returns:
        List<Dict>: A list of dictionaries containing the name, occupation, rating, and comment for each review.
    """
    # query the database
    connect = DbConnection.connector()["Reviews"]
    queryresults = connect.find({"Study_id": id,
                                 "Name": {"$exists": True},
                                 "Occupation": {"$exists": True},
                                 "Rating": {"$exists": True},
                                 "Comment": {"$exists": True}})
    # convert tot he output format
    reviewlist = []
    for review in queryresults:
        outdoc = dict()
        outdoc["name"] = review["Name"]
        outdoc["occupation"] = review["Occupation"]
        outdoc["rating"] = review["Rating"]
        outdoc["comment"] = review["Comment"]
        reviewlist += [outdoc]
    return reviewlist
