from app.db_connection import mongo

def get_user(email):
    # returns None if user is not found
    return mongo.db.users.find_one({'email': email})