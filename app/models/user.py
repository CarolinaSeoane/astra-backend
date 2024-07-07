class User:

    def __init__(self, _id, name, surname, email, profile_picture, permits, organizations=set()):
        self._id = _id
        self.name = name
        self.surname = surname
        self.email = email
        self.profile_picture = profile_picture
        self.organizations = organizations
        self.permits = permits
