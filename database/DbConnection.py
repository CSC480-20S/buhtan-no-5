from pymongo import MongoClient
import os
#This should be used to connect to the database remotely
#username and password should be called externally
class Connection():
    def connector(self):
        client = MongoClient(os.getenv('MongoURL'))  # Usr and pwd Needs to be externally called as well as auth
        db = client["StudyStore"]
        return db

# Examples of functions that can be performed on the database:
    def postdb(self,tb, info):
        connect = self.connector()
        locate = connect[tb]
        locate.insert_one(info)


    def editdb(self, tb, curr, new_data):
        connect = self.connector()[tb]
        connect.update_one(curr, new_data)


    def delete(self, tb, info):
        connect = self.connector()[tb]
        connect.delete_one(info)


if __name__ == '__main__':
    Connection().connector()
    post = {"id": 0, "Name": "Nahyro", "credits": 234, "Researcher": True}
    UPost = {"user_id": 0, "Name": "Nahyro", "credits": 234, "Researcher": True}
    APost = {"id": 0, "Name": "Nahyro", "email": "nmolina@oswego.edu", "auth_token": 92, "type": "Researcher"}
    SPost = {"study_id": 0, "Author": "Nahyro", "Author_id": 234, "price_in_credits": 23}

    Connection().postdb("Users", post)
    Connection().postdb("Upload", UPost)
    Connection().postdb("Account", APost)
    Connection().postdb("Studies", SPost)

