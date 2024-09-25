from bson import ObjectId
from enum import Enum

from app.services.mongoHelper import MongoHelper


class Color(Enum):
    BLUE = "astra-logo-blue"
    LIME = "astra-lime"
    GREEN = "astra-dark-green"
    PURPLE = "astra-dark-purple"
    RED = "astra-red"
    ORANGE = "astra-orange"
    YELLOW = "astra-yellow"


class Epic:

    def __init__(self, title, description, team, organization, priority, epic_color, creator, acceptance_criteria, business_value, status):
        self.title = title
        self.description = description
        self.creator = creator
        self.priority = priority
        self.epic_color = epic_color
        self.acceptance_criteria = acceptance_criteria
        self.business_value = business_value
        self.team = team
        self.organization = organization
        self.status = status

    @staticmethod
    def get_epics_from_organization(org_id):
        '''
        returns None if the organization has no epics
        '''
        filter = {'organization': ObjectId(org_id)}

        return MongoHelper().get_documents_by("epics", filter)
    
    @staticmethod
    def get_epics_from_team(org_id):
        '''
        returns None if the team has no epics
        '''
        filter = {'team': ObjectId(org_id)}

        return MongoHelper().get_documents_by("epics", filter)
    
    @staticmethod
    def create_epic(epic_document):
        return MongoHelper().create_document('epics', epic_document)
    
    @staticmethod
    def get_epic_fields(sections=False):
        epic_fields =  MongoHelper().get_documents_by('epic_fields', sort={'order': 1})
        if sections:
            epic_sections = {}
            for epic_field in epic_fields:
                sec = epic_sections.setdefault(epic_field["section"], [])
                sec.append(epic_field)
            return epic_sections
        return epic_fields
    
    @staticmethod
    def get_names_of_mandatory_fields():
        filter = { 'modifiable': 0 }
        projection = { 'value' }
        docs = MongoHelper().get_documents_by('epic_fields', filter=filter, sort={'order': 1}, projection=projection)
        return [doc['value'] for doc in docs]
    
    @classmethod
    def get_count_by_sprint(cls, sprint_name, team_id):
        match = {
            "sprint.name": sprint_name,
            "team": team_id
        }
        group = {
            "_id": "$epic.title",
            "count": { "$sum": 1 }
        }
        return MongoHelper().aggregate('stories', match, group)
