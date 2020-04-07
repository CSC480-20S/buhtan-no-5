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
