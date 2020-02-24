from pymongo import MongoClient
import os
# This should be used to connect to the database remotely
# username and password should be called externally


def connector():
    client = MongoClient(os.getenv('MongoURL))
    db = client["StudyStore"]
    return db


def delete(tb, info):
    connect = connector()[tb]
    connect.delete_many(info)


def edit(tb, curr, new_data):
    connect = connector()[tb]
    connect.update_many(curr, new_data)


def get(tb, info):
    connect = connector()
    locate = connect[tb]
    check = locate.find(info)
    return check


def post(tb, info):
    connect = connector()
    locate = connect[tb]
    if isinstance(info, list):
        locate.insert_many(info)
    else:
        locate.insert_one(info)


def filtered(tb, info):
    filler = get(tb, info)
    search = filler.sort(info, 1)
    return search


if __name__ == '__main__':
    connector()
    poster = {"id": 0, "Name": "Hey", "credits": 234, "Researcher": True}
    edits = {"$set": {"Name": "Canyon 123"}}
    find = {"Name": "Canyon 123"}
    delete = {"Name": {"$regex": "^H"}}

    post("Users", poster)
    edit("Users", poster, edits)
    time = get("Users", find)


