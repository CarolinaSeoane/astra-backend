from bson import ObjectId
from datetime import datetime
import pytz


from app.models.user import User
from app.services.mongoHelper import MongoHelper
from app.models.member import MemberStatus
class Team:

    def __init__(self, _id, name, organization, team_settings, member_status, members):
        self._id = _id
        self.name = name
        self.organization = organization
        self.team_settings = team_settings
        self.members = members
        self.member_status = member_status

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
            "status": status
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
            new_user.add_team(team)
        except Exception as e:
            print(f"Error adding new member to team: {e}")
            if added_to_team:
                cls.remove_member(team_id, new_user._id)
            return False
        return True

    @classmethod
    def remove_member(cls, team_id, member_id):
        print(f"type of member id {type(member_id)}")
        print(f"removing member {member_id} from team {team_id}")
        user = User.get_user_by({'_id': ObjectId(member_id)})
        print(f"type of user id {user}")
        filter = {'_id': ObjectId(team_id)}
        # update = {'$pull': {'members': {'_id': ObjectId("66a2e863493fe8221a338f0b")}}} # pull is used to remove a value from an existing array
        update = {'$pull': {'members': {'email': user["email"]}}}
        MongoHelper().update_collection('teams', filter, update)
        resp = User.remove_from_team(member_id, team_id)

    @classmethod
    def get_team_settings(cls, team_id):
        return cls.get_team(team_id)['team_settings']
    
    @classmethod
    def get_base_permissions(cls):
        return MongoHelper().get_collection('permissions')

    @classmethod
    def update_mandatory_fields(cls, team_id, settings):
        filter = {'_id': team_id}
        update = {'$set': {'team_settings.story_fields': settings}}
        MongoHelper().update_collection('teams', filter, update)

    @classmethod
    def update_sprint_set_up(cls, team_id, set_up):
        filter = {'_id': team_id}
        update = {'$set': {'team_settings.sprint_set_up': set_up}}
        MongoHelper().update_collection('teams', filter, update)

    @classmethod
    def update_ceremonies_settings(cls, team_id, ceremonies_settings):
        filter = {'_id': team_id}
        update = {'$set': {'team_settings.ceremonies': ceremonies_settings}}
        MongoHelper().update_collection('teams', filter, update)

    @classmethod
    def update_permissions(cls, team_id, permits):
        filter = {'_id': team_id}
        update = {'$set': {'team_settings.permits': permits}}
        MongoHelper().update_collection('teams', filter, update)
    
    @classmethod
    def get_organization(cls, team_id):
        return MongoHelper().get_document_by('teams', {'_id': ObjectId(team_id)}, projection={'organization'})['organization']
    
    @classmethod
    def is_user_part_of_team(cls, user_id, team_members):
        return user_id in [member['_id']['$oid'] for member in team_members] # TODO change id to _id
