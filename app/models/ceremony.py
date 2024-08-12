from bson import ObjectId
from app.services.mongoHelper import MongoHelper
from app.models.team import Team  # Asegúrate de importar la clase Team si la usas en esta clase

class Ceremony:

    def __init__(self, _id, name, date, in_progress):
        self._id = _id
        self.name = name
        self.date = date
        self.in_progress = in_progress

    @classmethod
    def get_ceremony(cls, ceremony_id):
        """
        Retrieves a ceremony by its ID. Returns None if not found.
        """
        # Convert the ID to ObjectId if it is not already
        if not isinstance(ceremony_id, ObjectId):
            ceremony_id = ObjectId(ceremony_id)
        
        filter = {'_id': ceremony_id}
        return MongoHelper().get_document_by('ceremonies', filter)

    @classmethod
    def get_all_ceremonies(cls, team_id):
        """
        Returns a list of ceremonies for a specific team.
        """
        team = Team.get_team(team_id)
        if team is None:
            return []
        return team.get('ceremonies', [])

    @staticmethod
    def update_ceremony(ceremony_id, update_data):
        """
        Updates a ceremony with the given ID using the provided update data.
        """
        # Convert the ID to ObjectId if it is not already
        if not isinstance(ceremony_id, ObjectId):
            ceremony_id = ObjectId(ceremony_id)
        
        filter = {'_id': ceremony_id}
        update = {'$set': update_data}
        return MongoHelper().update_collection('ceremonies', filter, update)

    @staticmethod
    def add_ceremony(ceremony_data):
        """
        Adds a new ceremony to the collection.
        """
        # Ensure that the ceremony_data has all required fields and convert necessary types
        # Add any additional validation if required
        return MongoHelper().add_new_element_to_collection('ceremonies', ceremony_data)

    @staticmethod
    def delete_ceremony(ceremony_id):
        """
        Deletes a ceremony by its ID.
        """
        # Convert the ID to ObjectId if it is not already
        if not isinstance(ceremony_id, ObjectId):
            ceremony_id = ObjectId(ceremony_id)

        filter = {'_id': ceremony_id}
        return MongoHelper().delete_element_from_collection('ceremonies', filter)