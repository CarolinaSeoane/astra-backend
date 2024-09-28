from bson import ObjectId
from datetime import datetime
import pytz

from app.models.user import User
from app.services.mongoHelper import MongoHelper
from app.models.configurations import MemberStatus
from app.services.google_meet import create_space
from app.models.configurations import Configurations


class Team:

    def __init__(self, _id, name, organization, ceremonies, sprint_set_up, mandatory_story_fields, permits, members):
        self._id = _id
        self.name = name
        self.organization = organization
        self.ceremonies = ceremonies
        self.sprint_set_up = sprint_set_up
        self.mandatory_story_fields = mandatory_story_fields
        self.permits = permits
        self.members = members

    @staticmethod
    def get_team(team_id):
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
            return []
        return team['members']
    
    @classmethod
    def add_member(cls, team_id, new_user, role, status=MemberStatus.PENDING.value):
        current_time = datetime.now(pytz.utc)
        team_member = {
            "_id": new_user._id,
            "username": new_user.username,
            "email": new_user.email,
            "profile_picture": new_user.profile_picture,
            "role": role,
            "member_status": status
            # "date": {
            #     "$date": current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00'
            # }
        }

        filter = {'_id': ObjectId(team_id)}
        update = {'$push': {'members': team_member}} # push is used to insert a new value to an existing array
    
        try:
            MongoHelper().update_collection('teams', filter, update) # check what this returns. maybe i dont have to do a get_teams after
            added_to_team = True
            team = cls.get_team(team_id)
            new_user.add_team(team, status)
        except Exception as e:
            print(f"Error adding new member to team: {e}")
            if added_to_team:
                cls.remove_member(team_id, new_user._id)
            return False
        return True

    @staticmethod
    def remove_member(team_id, member_id):
        print(f"removing member {member_id} from team {team_id}")
        user = User.get_user_by({'_id': ObjectId(member_id)})
        filter = {'_id': ObjectId(team_id)}
        # update = {'$pull': {'members': {'_id': ObjectId("66a2e863493fe8221a338f0b")}}} # pull is used to remove a value from an existing array
        update = {'$pull': {'members': {'email': user["email"]}}}
        MongoHelper().update_collection('teams', filter, update)
        resp = User.remove_from_team(member_id, team_id)

    @staticmethod
    def get_team_settings(team_id, section):
        projection = {'ceremonies', 'sprint_set_up', 'mandatory_story_fields', 'permits', 'members'}
        if section:
            projection = {section}
        settings = MongoHelper().get_document_by('teams', {'_id': ObjectId(team_id)}, projection=projection)
        return settings
    
    @staticmethod #Move to Configurations
    def get_base_permissions():
        return MongoHelper().get_collection('permissions')

    @staticmethod
    def update_mandatory_fields(team_id, settings):
        filter = {'_id': team_id}
        update = {'$set': {'mandatory_story_fields': settings}}
        MongoHelper().update_collection('teams', filter, update)

    @staticmethod
    def update_sprint_set_up(team_id, set_up):
        filter = {'_id': team_id}
        update = {'$set': {'sprint_set_up': set_up}}
        MongoHelper().update_collection('teams', filter, update)

    @staticmethod
    def update_ceremonies_settings(team_id, ceremonies_settings):
        filter = {'_id': team_id}
        update = {'$set': {'ceremonies': ceremonies_settings}}
        MongoHelper().update_collection('teams', filter, update)

    @staticmethod
    def update_permissions(team_id, permits):
        filter = {'_id': team_id}
        update = {'$set': {'permits': permits}}
        MongoHelper().update_collection('teams', filter, update)
    
    @staticmethod
    def get_organization(team_id):
        return MongoHelper().get_document_by('teams', {'_id': ObjectId(team_id)}, projection={'organization'})['organization']
    
    @staticmethod
    def is_user_part_of_team(user_id, team_members):
        return user_id in [member['_id']['$oid'] for member in team_members]
    
    @staticmethod
    def add_team(team_document):
        return MongoHelper().create_document('teams', team_document)
    
    @staticmethod
    def add_default_settings(team_id):
        '''
        Adds or overwrites team's settings with default settings from
        "default_settings" collection. Default settings do not include
        google Meet info and should be added separately
        '''
        # default_settings = MongoHelper().get_document_by('default_settings', {})
        default_settings = Configurations.get_default_settings()

        # ARREGLAR!!!!! cargar en 1 doc todo el cursor

        filter = {'_id': ObjectId(team_id)}
        update = {'$set': {default_settings}}
        return MongoHelper().update_collection('teams', filter, update)
    
    @staticmethod
    def set_up_google_meet_space(team_id, ceremony, access_token, refresh_token):
        '''
        Sets up a google meet space for the specified ceremony using
        google_meet service
        '''
        space = create_space(access_token, refresh_token)
        filter = {'_id':ObjectId(team_id)}
        update = {'$set': {f'ceremonies.{ceremony.lower()}.google_meet_config': space}}
        return MongoHelper().update_collection('teams', filter, update)
    