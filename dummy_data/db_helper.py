from app.db_connection import mongo


class DBHelper:

    def __init__(self):
        pass

    def post_to_collection(self, collection, data=None):
        return mongo.db[collection].insert_many(data)       

    def drop_db(self):
        mongo.cx.drop_database("astra")
