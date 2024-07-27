from bson import ObjectId, json_util
import json

from app.db_connection import mongo


class User:

    def __init__(self, name, surname, username, email, profile_picture, teams=list(), _id=ObjectId()):
        self._id = _id
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.profile_picture = profile_picture
        self.teams = teams

    @classmethod
    def get_user(cls, email):
        '''
        returns None if user is not found and dict if found
        '''
        user_data = mongo.db.users.find_one({'email': email})
        user_data = json_util.dumps(user_data)
        user_data = json.loads(user_data)
        
        return user_data

    @classmethod
    def is_user_in_team(cls, _id, team_id):
        '''
        returns False if user is not part of the team
        '''

        filter = {
            "_id": { "$eq": ObjectId(_id) },
            "teams": { "$elemMatch": {"_id": { "$eq": team_id }}} 
        }
        
        return mongo.db.users.count_documents(filter) > 0
    
    def save_user(self):
        mongo.db.users.insert_one(self.__dict__)
    
