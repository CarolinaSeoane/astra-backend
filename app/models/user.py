from app.db_connection import mongo
from bson import ObjectId

from app.utils import handle_object_id, handle_object_ids


class User:

    def __init__(self, name, surname, username, email, profile_picture, organizations=set(), _id=ObjectId()):
        self._id = _id
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.profile_picture = profile_picture
        self.organizations = organizations

    @classmethod
    def get_user(cls, email):
        '''
        returns None if user is not found
        '''
        user_data = mongo.db.users.find_one({'email': email})
        return User(**user_data) if user_data else None
    
    def from_obj_to_dict(self, convert_id_to_str=True):
        # Method used to convert the python object to a dict keeping all objectIds as ObjectId or strings
        return {
            '_id': handle_object_id(self._id, convert_id_to_str),
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'profile_picture': self.profile_picture,
            'organizations': handle_object_ids(self.organizations, convert_id_to_str)
        }
    
    def save_user(self):
        usr = self.from_obj_to_dict(False)
        mongo.db.users.insert_one(usr)
    
