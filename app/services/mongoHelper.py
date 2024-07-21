from bson import ObjectId, json_util
import json

from app.db_connection import mongo

class MongoHelper:

    def __init__(self):
        self.astra = mongo
    
    def get_document_by(self, collection_name, filter):
        document = self.astra.db[collection_name].find_one(filter)
        document = json_util.dumps(document)
        document = json.loads(document)
        return document

