from bson import ObjectId

from app.services.mongoHelper import MongoHelper
from app.models.configurations import Configurations, CollectionNames
from app.utils import mongo_query


EPICS_COL = CollectionNames.EPICS.value
STORIES_COL = CollectionNames.STORIES.value


class Epic:

    def __init__(self, title, description, team, organization, priority, epic_color,
                 creator, acceptance_criteria, business_value, status):
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
        return MongoHelper().get_documents_by(EPICS_COL, filter)

    @staticmethod
    def get_epics_from_team(org_id):
        '''
        returns None if the team has no epics
        '''
        filter = {'team': ObjectId(org_id)}
        return MongoHelper().get_documents_by(EPICS_COL, filter)

    @staticmethod
    @mongo_query
    def create_epic(epic_document):
        resp = MongoHelper().create_document(EPICS_COL, epic_document)
        return {
            "message": [resp.acknowledged],
            "status": 201
        }

    @staticmethod
    def get_epic_fields(sections=False):
        epic_fields =  Configurations.get_all_possible_epic_fields()['epic_fields']
        if sections:
            epic_sections = {}
            for epic_field in epic_fields:
                sec = epic_sections.setdefault(epic_field["section"], [])
                sec.append(epic_field)
            return epic_sections
        return epic_fields

    @staticmethod
    def get_names_of_mandatory_fields():
        docs =  Configurations.get_all_possible_epic_fields(True)['epic_fields']
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
        return MongoHelper().aggregate(STORIES_COL, match, group)
