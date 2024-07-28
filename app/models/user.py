from bson import ObjectId

from app.db_connection import mongo
from app.services.mongoHelper import MongoHelper


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
    def get_user_by(cls, filter):
        '''
        returns None if user is not found and dict if found
        '''
        return MongoHelper().get_document_by('users', filter)

    @classmethod
    def is_user_in_team(cls, _id, team_id):
        '''
        returns False if user is not part of the team
        '''
        # query = {
        #     "_id": ObjectId(_id),
        #     "teams._id": team_id
        # }

        filter = {
            "_id": { "$eq": ObjectId(_id) },
            "teams": { "$elemMatch": {"_id": { "$eq": team_id }}} 
        }
        
        return mongo.db.users.count_documents(filter) > 0 # TODO use mongoHelper
    
    def save_user(self):
        mongo.db.users.insert_one(self.__dict__) # TODO use mongoHelper

    def add_team(self, team):
        '''
        Add team to user's teams list
        '''
        new_team = {
            "id": team['_id'],
            "name": team['name']
        }
        filter = {'_id': ObjectId(self._id['$oid'])}
        update = {'$push': {'teams': new_team}}
        MongoHelper().update_collection('users', filter, update)

    @classmethod
    def remove_from_team(cls, user_id, team_id):
        '''
        Remove user from team
        '''
        filter = {'_id': ObjectId(user_id)}
        update = {'$pull': {'teams': {'_id': ObjectId(team_id)}}}
        MongoHelper().update_collection('users', filter, update)
