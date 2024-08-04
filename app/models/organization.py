from bson import ObjectId


class Organization:

    def __init__(self, name, epics, _id=ObjectId()):
        self._id = _id
        self.name = name
        self.epics = epics
