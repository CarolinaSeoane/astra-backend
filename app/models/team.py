from bson import ObjectId
from datetime import datetime
import pytz

from app.services.mongoHelper import MongoHelper


class Team:

    def __init__(self, _id, name, organization, team_settings, members):
        self._id = _id
        self.name = name
        self.organization = organization
        self.team_settings = team_settings
        self.members = members

    @classmethod
    def get_team(cls, team_id):
        '''
        returns None if team is not found and dict if found
        '''
        return MongoHelper().get_document_by('teams', {'_id': ObjectId(team_id)})

    @classmethod
    def get_team_members(cls, team_id):
        '''
        returns None if team is not found and list of dict if found
        '''
        team = cls.get_team(team_id)
        if team is None:
            return None
        return team['members']
    
    @classmethod
    def add_member(cls, team_id, new_user, role):
        current_time = datetime.now(pytz.utc)
        team_member = {
            "user": new_user._id,
            "username": new_user.username,
            "email": new_user.email,
            "profile_picture": new_user.profile_picture,
            "role": role,
            "date": current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00'
        }

        filter = {'_id': ObjectId(team_id)}
        update = {'$push': {'members': team_member}} # push is used to insert a new value to an existing array
    
        try:
            MongoHelper().update_collection('teams', filter, update) # check what this returns. maybe i dont have to do a get_teams after
            added_to_team = True
            team = cls.get_team(team_id)
            new_user.add_team(team)
        except Exception as e:
            print(f"Error adding new member to team: {e}")
            if added_to_team:
                cls.remove_member(team_id, new_user._id)
            return False
        return True

    @classmethod
    def remove_member(cls, team_id, member_id):
        '''
        returns True if member is removed and False if member is not found
        '''
        filter = {'_id': ObjectId(team_id)}
        update = {'$pull': {'members': {'user': ObjectId(member_id)}}} # pull is used to remove a value from an existing array