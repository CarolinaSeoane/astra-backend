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
    BEGINNING = "First day of sprint"
    END = "Last day of previous sprint"

class CollectionNames(Enum):
    CONFIGURATIONS = "configurations"
    EPICS = "epics"
    ORGANIZATIONS = "organizations"
    PERMISSIONS = "permissions"
    SPRINTS = "sprints"
    STORIES = "stories"
    TEAMS = "teams"
    USERS = "users"
    CEREMONIES = "ceremonies"

class CeremonyStatus(Enum):
    DONE = 'Done'
    NOT_HAPPENED_YET = 'Not happened yet'
    DIDNT_TAKE_PLACE = 'Did not take place'

CONFIGURATIONS_COL = CollectionNames.CONFIGURATIONS.value
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
