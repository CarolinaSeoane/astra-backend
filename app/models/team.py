from datetime import datetime
import pytz
from bson import ObjectId

from app.models.user import User
from app.services.mongoHelper import MongoHelper
from app.models.configurations import MemberStatus
from app.services.google_meet import create_space
from app.models.configurations import Configurations, CollectionNames, Role


TEAMS_COL = CollectionNames.TEAMS.value
PRODUCT_OWNER = Role.PRODUCT_OWNER.value


class Team:

    def __init__(self, _id, name, organization, ceremonies, sprint_set_up, 
                 mandatory_story_fields, permits, members, estimation_method):
        self._id = _id
        self.name = name
        self.organization = organization
        self.ceremonies = ceremonies
        self.sprint_set_up = sprint_set_up
        self.mandatory_story_fields = mandatory_story_fields
        self.permits = permits
        self.members = members
        self.estimation_method = estimation_method

    @staticmethod
    def get_team(team_id):
        '''
        returns None if team is not found and dict if found
        '''
        return MongoHelper().get_document_by(TEAMS_COL, {'_id': ObjectId(team_id)})

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

        added_to_team = False
        try:
            MongoHelper().update_document(TEAMS_COL, filter, update)
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
    def accept_member(user_email, team_id):
        filter={'_id': ObjectId(team_id), 'members.email': user_email}
        update={'$set': {'members.$.member_status': MemberStatus.ACTIVE.value, 'members.$.role': Role.DEV.value}}

        MongoHelper().update_document(TEAMS_COL, filter=filter, update=update)
        User.activate_team(user_email, team_id)
        return

    @staticmethod
    def remove_member(team_id, member_id):
        print(f"removing member {member_id} from team {team_id}")
        user = User.get_user_by({'_id': ObjectId(member_id)})
        filter = {'_id': ObjectId(team_id)}
        update = {'$pull': {'members': {'email': user["email"]}}}
        MongoHelper().update_document(TEAMS_COL, filter, update)
        User.remove_from_team(member_id, team_id)

    @staticmethod
    def get_team_settings(team_id, section=None):
        projection = {'ceremonies', 'sprint_set_up', 'mandatory_story_fields', 'permits', 'members', 'estimation_method'}
        if section:
            projection = {section}
        settings = MongoHelper().get_document_by(
            TEAMS_COL, {'_id': ObjectId(team_id)}, projection=projection
        )
        return settings

    @staticmethod #Move to Configurations
    def get_base_permissions():
        return MongoHelper().get_collection('permissions')

    @staticmethod
    def update_mandatory_fields(team_id, settings):
        filter = {'_id': team_id}
        update = {'$set': {'mandatory_story_fields': settings}}
        MongoHelper().update_document(TEAMS_COL, filter, update)

    @staticmethod
    def update_sprint_set_up(team_id, set_up):
        filter = {'_id': team_id}
        update = {'$set': {'sprint_set_up': set_up}}
        MongoHelper().update_document(TEAMS_COL, filter, update)

    @staticmethod
    def update_ceremonies_settings(team_id, ceremonies_settings):
        filter = {'_id': team_id}
        update = {'$set': {'ceremonies': ceremonies_settings}}
        MongoHelper().update_document(TEAMS_COL, filter, update)

    @staticmethod
    def update_permissions(team_id, permits):
        filter = {'_id': team_id}
        update = {'$set': {'permits': permits}}
        MongoHelper().update_document(TEAMS_COL, filter, update)

    @staticmethod
    def get_organization(team_id):
        return MongoHelper().get_document_by(
            TEAMS_COL, {'_id': ObjectId(team_id)}, projection={'organization'}
        )['organization']

    @staticmethod
    def is_user_part_of_team(user_id, team_members):
        return user_id in [member['_id']['$oid'] for member in team_members]

    @staticmethod
    def is_user_SM_of_team(user_id, team_id):
        filter = {
            '_id': ObjectId(team_id),
            'members': {
                '$elemMatch': {
                    '_id': ObjectId(user_id),
                    'role': Role.SCRUM_MASTER.value
                }
            }
        }
        return MongoHelper().document_exists(TEAMS_COL, filter)

    @staticmethod
    def add_team(team_document):
        return MongoHelper().create_document(TEAMS_COL, team_document)

    @staticmethod
    def add_default_settings(team_id):
        '''
        Adds or overwrites team's settings with default settings from
        "default_settings" collection. Default settings do not include
        google Meet info and should be added separately
        '''
        default_settings_docs = Configurations.get_default_settings()
        default_settings = {}

        for set in default_settings_docs:
            setting = set['value']
            default_settings[setting] = set[setting]

        filter = {'_id': ObjectId(team_id)}
        update = {'$set': default_settings}
        res = MongoHelper().update_document(TEAMS_COL, filter, update)
        print(res)

    @staticmethod
    def set_up_google_meet_space(team_id, ceremony, access_token, refresh_token):
        '''
        Sets up a google meet space for the specified ceremony using
        google_meet service
        '''
        space = create_space(access_token, refresh_token)
        filter = {'_id': ObjectId(team_id)}
        update = {'$set': {f'ceremonies.{ceremony.lower()}.google_meet_config': space}}
        return MongoHelper().update_document(TEAMS_COL, filter, update)

    @staticmethod
    def get_product_owner(team_id):
        team = Team.get_team(ObjectId(team_id))
        if team:
            for member in team.get("members", []):
                if member.get("role") == PRODUCT_OWNER:
                    po_id = member.get("_id")
                    if isinstance(po_id, dict) and "$oid" in po_id:
                        return ObjectId(po_id["$oid"])
                    return po_id
        return None

    @staticmethod
    def get_member_role(team_id, email):
        match = {
            "_id": ObjectId(team_id),
            "members": {"$elemMatch": {"email": email}}
        }
        projection = {"members.role.$": 1}
        return MongoHelper().get_document_by(
            TEAMS_COL, match, projection=projection
        )["members"][0]["role"]

    @staticmethod
    def get_permissions_value_based_on_role(team_id, role):
        match = {
            '_id': ObjectId(team_id),
            "permits": {"$elemMatch": {"role": role}}
        }
        projection = {"permits.options.$": 1}
        return MongoHelper().get_document_by(
            TEAMS_COL, match, projection=projection
        )["permits"][0]["options"]

    @staticmethod
    def is_member_authorized(team_id, role, action):
        available_actions = Team.get_permissions_value_based_on_role(
            team_id, role
        )
        return action in available_actions

    @staticmethod
    def update_members_role(team_id, roles):
        for role_change in roles:
            match = {
                "_id": ObjectId(team_id),
                "members._id": ObjectId(role_change["_id"])
            }
            update = {
                "$set": {"members.$.role": role_change["role"]}
            }
            MongoHelper().update_document(TEAMS_COL, match, update)
