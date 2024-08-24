from bson import ObjectId
import datetime
from app import db_connection

class Ceremony:
    def __init__(self, team_id, name, start_time, attendees=None):
        self.team_id = team_id
        self.name = name
        self.start_time = start_time
        self.attendees = attendees or []

    @staticmethod
    def get_by_id(ceremony_id):
        return db_connection.db.ceremonies.find_one({"_id": ObjectId(ceremony_id)})

    @staticmethod
    def get_by_team_id(team_id):
        return list(db_connection.db.ceremonies.find({"team_id": team_id}))

    def save(self):
        data = self.__dict__.copy()
        if hasattr(self, '_id'):
            db_connection.db.ceremonies.update_one({"_id": self._id}, {"$set": data})
        else:
            self._id = db_connection.db.ceremonies.insert_one(data).inserted_id

    @staticmethod
    def update_ceremony_time(ceremony_id, new_time):
        db_connection.db.ceremonies.update_one({"_id": ObjectId(ceremony_id)}, {"$set": {"start_time": new_time}})

    @staticmethod
    def update_attendance(ceremony_id, user_id, confirmed, justification=None):
        db_connection.db.ceremonies.update_one(
            {"_id": ObjectId(ceremony_id), "attendees.user_id": user_id},
            {"$set": {
                "attendees.$.confirmed": confirmed,
                "attendees.$.justification": justification
            }}
        )
        db_connection.db.ceremonies.update_one(
            {"_id": ObjectId(ceremony_id)},
            {"$push": {
                "attendees": {
                    "user_id": user_id,
                    "confirmed": confirmed,
                    "justification": justification
                }
            }},
            upsert=True
        )

    @staticmethod
    def delete(ceremony_id):
        db_connection.db.ceremonies.delete_one({"_id": ObjectId(ceremony_id)})