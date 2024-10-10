import json
from bson import json_util

from app.db_connection import mongo


class MongoHelper:

    def __init__(self):
        self.astra = mongo

    def get_collection(self, collection_name):
        return self.get_documents_by(collection_name, {})

    def get_document_by(self, collection_name, filter, sort=None, projection=None):
        document = self.astra.db[collection_name].find_one(filter, sort=sort, projection=projection)
        document = json_util.dumps(document)
        document = json.loads(document)
        return document

    def get_documents_by(self, collection_name, filter=None, sort=None, projection=None):
        documents = self.astra.db[collection_name].find(filter, sort=sort, projection=projection)
        documents = json_util.dumps(documents)
        documents = json.loads(documents)
        return documents

    def add_new_element_to_collection(self, collection_name, element):
        return self.astra.db[collection_name].insert_one(element)

    def update_document(self, collection_name, filter, update):
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

    def create_document(self, collection_name, document):
        return self.astra.db[collection_name].insert_one(document)

    def aggregate(self, collection_name, match, group, unwind=None, **kwargs):
        '''
        Executes an aggregation pipeline sequentially, starting with the match stage,
        followed by the group stage, and finally the sort stage. If sorting before grouping 
        is required, the code will need to be refactored to accommodate that.
        Only use the following values for kwargs:
            - sort
            - project
        '''
        pipeline = [{"$match": match}, {"$group": group}]
        if unwind:
            pipeline = [{"$match": match}, {"$unwind": unwind}, {"$group": group}]
        for key, value in kwargs.items():
            name = f"${key}"
            pipeline.append({name: value})
        return self.astra.db[collection_name].aggregate(pipeline)

    def replace_document(self, collection_name, filter, new_document):
        return self.astra.db[collection_name].replace_one(filter, new_document)
