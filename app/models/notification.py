from bson import ObjectId
from app.services.mongoHelper import MongoHelper
import datetime

class Notification:

    def __init__(self, user_id, message, story_id, creator, assigned_to=None, created_at=None, viewed=False, _id=ObjectId()):
        self._id = _id
        self.user_id = user_id
        self.message = message
        self.story_id = story_id
        self.creator = creator
        self.assigned_to = assigned_to
        self.created_at = created_at or datetime.datetime.now()
        self.viewed = viewed  # Nuevo campo

    @classmethod
    def create_notification(cls, notification_data):
        return MongoHelper().create_document('notifications', notification_data)

    @classmethod
    def get_notifications_for_user(cls, user_id):
        filter_criteria = {
            "$or": [
                {"user_id": ObjectId(user_id)},  # Notificaciones dirigidas al usuario
                {"assigned_to": ObjectId(user_id)},  # Notificaciones asignadas al usuario
                {"creator": ObjectId(user_id)}  # Notificaciones donde el usuario es el creador
            ]
        }
        return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort={'created_at': -1})

    @classmethod
    def get_creator_notifications(cls, user_id):
        filter_criteria = {
            "creator": ObjectId(user_id)  # Filtrar donde el usuario es el creador
        }
        return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort={'created_at': -1})

    @classmethod
    def get_assigned_user_notifications(cls, user_id):
        filter_criteria = {
            "assigned_to": ObjectId(user_id)  # Filtrar por notificaciones asignadas al usuario
        }
        return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort={'created_at': -1})

    @classmethod
    def get_all_notifications(cls, user_id):
        filter_criteria = {
            "$or": [
                {"user_id": ObjectId(user_id)},  # Notificaciones dirigidas al usuario
                {"assigned_to": ObjectId(user_id)},  # Notificaciones asignadas al usuario
                {"creator": ObjectId(user_id)}  # Notificaciones donde el usuario es el creador
            ]
        }
        return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort={'created_at': -1})

    @classmethod
    def get_po_notifications(cls, user_id):
        filter_criteria = {
            "po_id": ObjectId(user_id),  # Ajusta según tu estructura de datos
            "notification_type": "product_related"
        }
        return cls.get_notifications_with_filter(filter_criteria)
    
    #@classmethod
    #def mark_as_viewed(cls, user_id, notification_ids):
    #    mongo_helper = MongoHelper()
        
        # Convertir los IDs de notificaciones a ObjectId
    #    try:
    #        notification_ids = [ObjectId(id) for id in notification_ids]
    #        user_id = ObjectId(user_id)
    #    except Exception as e:
    #        raise ValueError("Invalid ID format")

    #    filter = {
    #        "_id": {"$in": notification_ids},
    #        "user_id": user_id
    #    }
    #    update = {"$set": {"viewed": True}}

        # Actualizar las notificaciones en la base de datos
    #    result = mongo_helper.update_collection('notifications', filter, update)
        
    #    return result
    
    @classmethod
    def mark_notifications_as_viewed(cls, user_id, team_id, filter_type):
        filter_criteria = {"viewed": False}

        if filter_type == 'assigned':
            filter_criteria["assigned_to"] = ObjectId(user_id)
        elif filter_type == 'creator':
            filter_criteria["creator"] = ObjectId(user_id)
        else:
            filter_criteria["$or"] = [
                {"user_id": ObjectId(user_id)},
                {"assigned_to": ObjectId(user_id)},
                {"creator": ObjectId(user_id)}
            ]

        mongo_helper = MongoHelper()
        mongo_helper.astra.db['notifications'].update_many(
            filter_criteria,
            {"$set": {"viewed": True}}
        )
    @classmethod
    def count_unread_notifications(cls, user_id, team_id):
        filter_criteria = {
            "$or": [
                {"user_id": ObjectId(user_id)},
                {"assigned_to": ObjectId(user_id)},
                {"creator": ObjectId(user_id)}
            ],
                "viewed": False
        }
        mongo_helper = MongoHelper()
        return mongo_helper.astra.db['notifications'].count_documents(filter_criteria)
    
    @classmethod
    def count_assigned_notifications(cls, user_id, team_id):
        filter_criteria = {
            "assigned_to": ObjectId(user_id),
            "viewed": False
        }
        mongo_helper = MongoHelper()
        return mongo_helper.astra.db['notifications'].count_documents(filter_criteria)

    @classmethod
    def count_created_notifications(cls, user_id, team_id):
        filter_criteria = {
            "creator": ObjectId(user_id),
            "viewed": False
        }
        mongo_helper = MongoHelper()
        return mongo_helper.astra.db['notifications'].count_documents(filter_criteria)

    @classmethod
    def count_all_notifications(cls, user_id, team_id):
        filter_criteria = {
            "$or": [
                {"user_id": ObjectId(user_id)},
                {"assigned_to": ObjectId(user_id)},
                {"creator": ObjectId(user_id)}
            ],
            "viewed": False 
        }
        mongo_helper = MongoHelper()
        return mongo_helper.astra.db['notifications'].count_documents(filter_criteria)