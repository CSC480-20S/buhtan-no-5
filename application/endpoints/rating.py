from database import DbConnection


def ratingsys(id, user, name, rate, comment):
    """Creates a review for a study and updates that study's rating.
    If the user is submitting a duplicate review (same study), the previous review will be overwritten.

    Args:
         id (Integer): The identifier for the study being reviewed.
         user (String): The identifier for the user making the review.
         name (String): The name of the user, as it should be displayed on the review.
         rate (Integer): The rating the user is applying to the study.
         comment (String): The comment the user has about the study.

    Returns:
        Nothing.
    """
    connect = DbConnection.connector()
    review = connect["Reviews"]
    # post the review, overwriting any existing review
    review.update_one({"Study_id": id, "User_id": user},
                      {"Study_id": id, "User_id": user, "Name": name, "Rating": rate, "Comment": comment},
                      upsert=True)

    # find the new overall rating
    query = review.find({"Study_id": id})
    ratelist = []
    for rates in query:
        ratelist.append(rates["Rating"])
    average = sum(ratelist) / len(ratelist)  # Gets the average rating of this study
    average = round(average)  # this average is then converted to a whole number

    # update the rating for the study itself
    rater = connect["Studies"]
    rater.update_one({ "Study_id": id}, {"$set": {"Rating": average}})

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
    queryresults = connect.find({"Study_id": study_id,
                                 "Name": {"$exists": True},
                                 "Rating": {"$exists": True},
                                 "Comment": {"$exists": True}})
    # convert tot he output format
    reviewlist = []
    for review in queryresults[:]:
        outdoc = dict()
        outdoc["name"] = review["Name"]
        outdoc["rating"] = review["Rating"]
        outdoc["comment"] = review["Comment"]
        reviewlist += [outdoc]
    return reviewlist
