from bson import ObjectId
from enum import Enum

from app.services.mongoHelper import MongoHelper

class Color(Enum):
    BLACK = "Black"
    BLUE = "Blue"
    GREEN = "Green"
    PURPLE = "Purple"
    RED = "Red"
    ORANGE = "Orange"
    YELLOW = "Yellow"

class Epic:

    def __init__(self, title, description, team, organization, priority, color, creator):
        self.title = title
        self.description = description
        self.team = team
        self.priority = priority
        self.organization = organization
        self.color = color
        self.creator = creator

    @classmethod
    def get_epics_from_organization(cls, org_id):
        '''
        returns None if the organization has no epics
        '''
        filter = {'organization': ObjectId(org_id)}

        return MongoHelper().get_documents_by("epics", filter)
    
    @classmethod
    def create_epic(cls, epic_document):
        return MongoHelper().create_document('epics', epic_document)
