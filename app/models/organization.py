from bson import ObjectId

from app.services.mongoHelper import MongoHelper


class Organization:

    def __init__(self, name, _id=ObjectId()):
        self._id = _id
        self.name = name

    @staticmethod
    def get_organization_by(filter):
        '''
        returns None if organization is not found and dict if found
        '''
        return MongoHelper().get_document_by('organizations', filter)