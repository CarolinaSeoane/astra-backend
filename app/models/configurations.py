from enum import Enum

from app.services.mongoHelper import MongoHelper


class Estimation(Enum):
    FIBONACCI = "Fibonacci"
    SIZES = "Sizes"
    PLANNING_POKER = "Planning poker"
    HOURS = "Hours"
    DAYS = "Days"

class Color(Enum):
    BLUE = "astra-logo-blue"
    LIME = "astra-lime"
    GREEN = "astra-dark-green"
    PURPLE = "astra-dark-purple"
    RED = "astra-red"
    ORANGE = "astra-orange"
    YELLOW = "astra-yellow"
    PINK = "astra-pink"

class Role(Enum):
    SCRUM_MASTER = "Scrum Master"
    PRODUCT_OWNER = "Product Owner"
    DEV = "Developer"

class MemberStatus(Enum):
    ACTIVE = "Active"
    PENDING = "Pending"

class Status(Enum):
    DOING = "Doing"
    NOT_STARTED = "Not Started"
    BLOCKED = "Blocked"
    DONE = "Done"

class Type(Enum):
    BUGFIX = "Bugfix"
    FEATURE = "Feature"
    DISCOVERY = "Discovery"
    DEPLOYMENT = "Deployment"

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITIC = "Critic"

class SprintStatus(Enum):
    CURRENT = "Current"
    FINISHED = "Finished"
    FUTURE = "Future"
    ACTIVE = "Active" # Used for backlog

class CeremonyType(Enum):
    PLANNING = "Planning"
    STANDUP = "Standup"
    RETRO = "Retrospective"

class CeremonyStartOptions(Enum):
    BEGINNING = "first_day_of_sprint"
    END = "last_day_of_sprint"

class CollectionNames(Enum):
    CONFIGURATIONS = "configurations"
    EPICS = "epics"
    ORGANIZATIONS = "organizations"
    PERMISSIONS = "permissions"
    SPRINTS = "sprints"
    STORIES = "stories"
    TEAMS = "teams"
    USERS = "users"
    NOTIFICATIONS = "notifications"
    CEREMONIES = "ceremonies"
    POST_ITS = "post_its"
    BOARDS = "boards"
    MODIFIED_STORIES = "modified_stories"

class CeremonyStatus(Enum):
    CONCLUDED = 'concluded'
    NOT_HAPPENED_YET = 'not_happened_yet'
    DIDNT_TAKE_PLACE = 'did_not_take_place'

class GoogleMeetDataStatus(Enum):
    UNAVAILABLE = 'Unavailable'

CONFIGURATIONS_COL = CollectionNames.CONFIGURATIONS.value

PERMISSIONS_COL = CollectionNames.PERMISSIONS.value

class Configurations:
    def __init__(self, _id, key, value):
        self._id = _id
        self.key = key
        self.value = value

    @staticmethod
    def get_estimation_method_options(estimation_method):
        '''
        returns None if estimation_method is not found and dict if found
        '''
        return MongoHelper().get_document_by(
            CONFIGURATIONS_COL,
            {'key': 'estimation_methods', 'value': estimation_method}
        )

    @staticmethod
    def get_all_possible_story_fields():
        return MongoHelper().get_document_by(
            CONFIGURATIONS_COL,
            {'key': 'all_possible_fields', 'value': 'story_fields'},
            sort={'story_fields.order': 1}
        ) # creo que el sort no esta funcionando

    @staticmethod
    def get_all_possible_epic_fields(only_the_names=False):
        filter = {'key': 'all_possible_fields', 'value': 'epic_fields'}
        projection = {}
        if only_the_names:
            filter['epic_fields.modifiable'] = 0
            projection = { 'epic_fields.value' }
        return MongoHelper().get_document_by(
            CONFIGURATIONS_COL,
            filter, sort={'epic_fields.order': 1},
            projection=projection
        ) # creo que el sort no esta funcionando

    @staticmethod
    def get_default_settings():
        return MongoHelper().get_documents_by(
            CONFIGURATIONS_COL,
            {'key': 'default_settings'}
        )

    @staticmethod
    def get_permissions_label(role, permissions_value=None):
        res = MongoHelper().get_collection(PERMISSIONS_COL)[0]
        if not res:
            return []

        labels = []
        options = res["options"]
        for option in options:
            if option["role"] == role:
                for action in option["actions"]:
                    if permissions_value is None or action["value"] in permissions_value:
                        labels.append({
                            "label": action["label"],
                            "description": action["description"]
                        })
        return labels
