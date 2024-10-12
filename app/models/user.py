from bson import ObjectId

from app.services.mongoHelper import MongoHelper
from app.models.configurations import MemberStatus, CollectionNames


USERS_COL = CollectionNames.USERS.value

class User:

    def __init__(
            self, name, surname, username, email, profile_picture, access_token=None,
            refresh_token=None, teams=list(), _id=ObjectId()
        ):
        self._id = _id
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.profile_picture = profile_picture
        self.teams = teams
        self.access_token = access_token
        self.refresh_token = refresh_token

    @staticmethod
    def get_user_by(filter, get_google_tokens=False):
        '''
        returns None if user is not found and dict if found
        '''
        projection={}
        if not get_google_tokens:
            projection={'access_token': False, 'refresh_token': False}
        return MongoHelper().get_document_by(USERS_COL, filter, projection=projection)

    @staticmethod
    def is_user_in_team(_id, team_id, status=MemberStatus.ACTIVE.value):
        '''
        returns False if user is not part of the team
        '''
        filter = {
            "_id": ObjectId(_id),
            # "teams._id": team_id,
            # "member_status": status
            "teams": { "$elemMatch": {"_id": ObjectId(team_id) , "member_status": status}},
        }
        # filter = {
        #     "_id": { "$eq": ObjectId(_id) },
        #     "teams": { "$elemMatch": {"_id": { "$eq": team_id }}},
        #     "member_status": status
        # }
        return MongoHelper().document_exists(USERS_COL, filter)

    def save_user(self):
        MongoHelper().add_new_element_to_collection(USERS_COL, self.__dict__)

    def add_team(self, team, status=MemberStatus.PENDING.value):
        '''
        Add team to user's teams list.
        This list contains the teams for which the user is an active or pending member.
        When the SM adds a user to a team -> use status = ACTIVE (does not require approval)
        When the user requests to join a team -> use status = PENDING
        '''
        new_team = {
            "_id": ObjectId(team['_id']['$oid']),
            "name": team['name'],
            "member_status": status
        }
        filter = {'_id': ObjectId(self._id['$oid'])}
        update = {'$push': {'teams': new_team}}
        return MongoHelper().update_collection(USERS_COL, filter, update)

    @staticmethod
    def remove_from_team(user_id, team_id):
        '''
        Remove user from team
        '''
        filter = {'_id': ObjectId(user_id)}
        update = {'$pull': {'teams': {'_id': ObjectId(team_id)}}}
        MongoHelper().update_collection(USERS_COL, filter, update)
