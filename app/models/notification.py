from bson import ObjectId
from app.services.mongoHelper import MongoHelper
import datetime

class Notification:

    def __init__(self, user_id, message, story_id, creator, team_id, assigned_to=None, created_at=None, viewed=False, _id=ObjectId()):
        self._id = _id
        self.user_id = user_id
        self.message = message
        self.story_id = story_id
        self.creator = creator
        self.team_id = team_id  
        self.assigned_to = assigned_to
        self.created_at = created_at or datetime.datetime.now()
        self.viewed = viewed

    @classmethod
    def create_notification(cls, notification_data):
        return MongoHelper().create_document('notifications', notification_data)
    
    @classmethod
    def create_assigned_notification(cls, story, team_id):
        assigned_user_id_obj = story.get('assigned_to', {}).get('_id', {})
        assigned_user_id_str = cls._extract_id_string(assigned_user_id_obj)

        if assigned_user_id_str and len(assigned_user_id_str) == 24:
            assigned_user_id = ObjectId(assigned_user_id_str)
            notification_data = {
                'user_id': assigned_user_id,
                'message': f"Has sido asignado a la historia {story.get('title', 'No Title')}",
                'story_id': story.get('_id', 'No ID'),
                'creator': cls._extract_id_string(story.get('creator', {}).get('_id', '')),
                'assigned_to': assigned_user_id,
                'team_id': team_id,  
                'created_at': datetime.datetime.now().isoformat(),
                'viewed': False 
            }
            cls.create_notification(notification_data)

    @classmethod
    def create_creator_notification(cls, story, team_id):
        creator_id_obj = story.get('creator', {}).get('_id', {})
        creator_id_str = cls._extract_id_string(creator_id_obj)

        if creator_id_str and len(creator_id_str) == 24:
            creator_id = ObjectId(creator_id_str)
            notification_data = {
                'user_id': creator_id,
                'message': f"Has creado la historia {story.get('title', 'No Title')}",
                'story_id': story.get('_id', 'No ID'),
                'creator': creator_id,
                'assigned_to': None, 
                'team_id': team_id,  
                'created_at': datetime.datetime.now().isoformat(),
                'viewed': False 
            }
            cls.create_notification(notification_data)

    @classmethod
    def _extract_id_string(cls, id_value):
        if isinstance(id_value, dict) and '$oid' in id_value:
            return id_value['$oid']
        elif isinstance(id_value, str):
            return id_value
        return ''
            
    @classmethod
    def get_notifications_for_user(cls, user_id, team_id):
        filter_criteria = {
            "$or": [
                {"user_id": ObjectId(user_id)},
                {"assigned_to": ObjectId(user_id)},
                {"creator": ObjectId(user_id)}
            ],
            "team_id": ObjectId(team_id)  
        }
        return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort={'created_at': -1})

    @classmethod
    def get_creator_notifications(cls, user_id, team_id):
        filter_criteria = {
            "creator": ObjectId(user_id),
            "team_id": ObjectId(team_id)  
        }
        return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort={'created_at': -1})

    @classmethod
    def get_assigned_user_notifications(cls, user_id, team_id):
        filter_criteria = {
            "assigned_to": ObjectId(user_id),
            "team_id": ObjectId(team_id) 
        }
        return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort={'created_at': -1})

    @classmethod
    def get_all_notifications(cls, user_id, team_id):
        filter_criteria = {
            "$or": [
                {"user_id": ObjectId(user_id)},
                {"assigned_to": ObjectId(user_id)},
                {"creator": ObjectId(user_id)}
            ],
            "team_id": ObjectId(team_id)  
        }
        return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort={'created_at': -1})

    @classmethod
    def mark_notifications_as_viewed(cls, user_id, team_id, filter_type):
        filter_criteria = {"viewed": False, "team_id": ObjectId(team_id)}  

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
            "team_id": ObjectId(team_id),  
            "viewed": False
        }
        mongo_helper = MongoHelper()
        return mongo_helper.astra.db['notifications'].count_documents(filter_criteria)
    
    @classmethod
    def count_assigned_notifications(cls, user_id, team_id):
        filter_criteria = {
            "assigned_to": ObjectId(user_id),
            "team_id": ObjectId(team_id),  
            "viewed": False
        }
        mongo_helper = MongoHelper()
        return mongo_helper.astra.db['notifications'].count_documents(filter_criteria)

    @classmethod
    def count_created_notifications(cls, user_id, team_id):
        filter_criteria = {
            "creator": ObjectId(user_id),
            "team_id": ObjectId(team_id), 
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
            "team_id": ObjectId(team_id),  
            "viewed": False 
        }
        mongo_helper = MongoHelper()
        return mongo_helper.astra.db['notifications'].count_documents(filter_criteria)

    @classmethod
    def get_notifications_by_story_ids(cls, story_ids, team_id):

        notifications = MongoHelper().get_documents_by(
            'notifications',
            filter={'story_id': {'$in': story_ids}, 'team_id': ObjectId(team_id)}
        )
        return notifications
    
@classmethod
def get_subscribed_notifications(cls, user_id, team_id):
    filter_criteria = {
        "user_id": ObjectId(user_id),
        "team_id": ObjectId(team_id) 
    }
    
    return MongoHelper().get_documents_by('notifications', filter=filter_criteria, sort=[('created_at', -1)])  # Asegúrate de que sort sea una lista de tuplas

@classmethod
def get_team_story_edits(cls, team_id):
    
    filter_criteria = {
        "team_id": ObjectId(team_id)  
    }
    return MongoHelper().get_documents_by('notifications', filter=filter_criteria)
