from bson import ObjectId

from app.services.mongoHelper import MongoHelper

class Epic:

    def __init__(self, title, description, team, organization, priority):
        self.title = title
        self.description = description
        self.team = team
        self.priority = priority
        self.organization = organization

    @classmethod
    def get_epics_from_organization(cls, org_id):
        '''
        returns None if the organization has no epics
        '''
        filter = {'organization': ObjectId(org_id)}

        return MongoHelper().get_documents_by("epics", filter)
