from bson import json_util
import json

from app.db_connection import mongo


class MongoHelper:

    def __init__(self):
        self.astra = mongo

    def get_collection(self, collection_name):
        return self.get_document_by(collection_name, {})
    
    def get_document_by(self, collection_name, filter, sort=None):
        document = self.astra.db[collection_name].find_one(filter, sort=sort)
        document = json_util.dumps(document)
        document = json.loads(document)
        return document
    
    def get_documents_by(self, collection_name, filter=None, sort=None):
        documents = self.astra.db[collection_name].find(filter, sort=sort)
        documents = json_util.dumps(documents)
        documents = json.loads(documents)
        return documents
    
    def get_documents_grouped_by(self, collection_name, group_by):
        documents = self.astra.db[collection_name].aggregate(group_by)
        documents = json_util.dumps(documents)
        documents = json.loads(documents)
        return documents
    
    def add_new_element_to_collection(self, collection_name, element):
        return self.astra.db[collection_name].insert_one(element)
    
    def update_collection(self, collection_name, filter, update):
        '''
        filter refers to the document to be updated
        update refers to the field and values to be updated and how they should be updated

        Example:
        filter = {'name' : 'Bagels N Buns'}
        update = {'$set': {'name': 'Bagels & Buns'}} 
        this would update the name of the document with name 'Bagels N Buns' to 'Bagels & Buns'
        '''
        return self.astra.db[collection_name].update_one(filter, update)

    def delete_element_from_collection(self, collection_name, filter):
        return self.astra.db[collection_name].delete_one(filter) # doing .deleted_count will return the number of documents deleted
    
    def document_exists(self, collection_name, filter):
        '''
        returns False if no documents match the query
        '''
        return self.astra.db[collection_name].count_documents(filter) > 0
