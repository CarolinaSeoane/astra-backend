from app.db_connection import mongo

class User:

    def __init__(self, _id, name, surname, email, profile_picture, organizations=set()):
        self._id = _id
        self.name = name
        self.surname = surname
        self.email = email
        self.profile_picture = profile_picture
        self.organizations = organizations

    @classmethod
    def from_dict_to_obj(cls, user_data):
        if user_data:
            return cls(
                _id=user_data.get('_id'),
                name=user_data.get('name'),
                surname=user_data.get('surname'),
                email=user_data.get('email'),
                profile_picture=user_data.get('profile_picture'),
                organizations=set(user_data.get('organizations', []))
            )
        return None

    @classmethod
    def get_user(cls, email):
        # returns None if user is not found
        user_data = mongo.db.users.find_one({'email': email})
        return cls.from_dict_to_obj(user_data)
    
    def from_obj_to_dict(self, remove_object_ids=True):
        # Method used to convert the python object to a dict keeping all objectIds as ObjectId or strings
        return {
            '_id': str(self._id) if remove_object_ids else self._id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'profile_picture': self.profile_picture,
            'organizations': [str(org_id) for org_id in list(self.organizations)] if remove_object_ids else list(self.organizations)
        }
    
