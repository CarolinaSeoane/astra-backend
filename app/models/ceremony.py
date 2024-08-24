from bson import ObjectId
import datetime
from app import db_connection  # Importa db_connection desde donde esté configurado

class Ceremony:
    def __init__(self, team_id, name, start_time):
        self.team_id = team_id
        self.name = name
        self.start_time = start_time

    @staticmethod
    def get_by_id(ceremony_id):
        return db_connection.db.ceremonies.find_one({"_id": ObjectId(ceremony_id)})

    @staticmethod
    def get_by_team_id(team_id):
        return list(db_connection.db.ceremonies.find({"team_id": team_id}))

    def save(self):
        if hasattr(self, '_id'):
            db_connection.db.ceremonies.update_one({"_id": self._id}, {"$set": self.__dict__})
        else:
            self._id = db_connection.db.ceremonies.insert_one(self.__dict__).inserted_id

    @staticmethod
    def update_ceremony_time(ceremony_id, new_time):
        db_connection.db.ceremonies.update_one({"_id": ObjectId(ceremony_id)}, {"$set": {"start_time": new_time}})

    @staticmethod
    def delete(ceremony_id):
        db_connection.db.ceremonies.delete_one({"_id": ObjectId(ceremony_id)})