from bson import ObjectId, json_util
import json

from app.db_connection import mongo
from app.services.mongoHelper import MongoHelper


class Team:

    def __init__(self, _id, name, logo, organization, team_settings, members):
        self._id = _id
        self.name = name
        self.logo = logo
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
