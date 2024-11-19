import datetime
from bson import ObjectId

from app.models.configurations import CollectionNames
from app.services.mongoHelper import MongoHelper
from app.utils import try_to_convert_to_object_id


NOTIFICATIONS_COL = CollectionNames.NOTIFICATIONS.value
STORIES_COL = CollectionNames.STORIES.value


class Notification:

    def __init__(self, user_id, message, story_id, creator, team_id, assigned_to=None,
                 created_at=None, viewed_by=None, _id=ObjectId()):
        self._id = _id
        self._id = _id
        self.user_id = user_id
        self.message = message
        self.story_id = story_id
        self.creator = creator
        self.team_id = team_id
        self.assigned_to = assigned_to
        self.created_at = created_at or datetime.datetime.now()
        self.viewed_by = viewed_by or []

    @staticmethod
    def create_notification(owner_id, msg, story, assigned_to, team_id, title):
        owner_id = try_to_convert_to_object_id(owner_id)
        assigned_to = try_to_convert_to_object_id(assigned_to)
        notification_data = {
            'user_id': owner_id,
            'title': title,
            'message': msg,
            'story_id': story['_id'],
            'creator': ObjectId(story['creator']['_id']['$oid']),
            'assigned_to': assigned_to,
            'team_id': team_id,  
            'created_at': datetime.datetime.now().isoformat(),
            'viewed_by': []
        }
        # print(f"creating notification with payload {notification_data}")
        return MongoHelper().create_document(NOTIFICATIONS_COL, notification_data)

    @staticmethod
    def create_assigned_notification(story, team_id):
        assigned_to = story.get('assigned_to', {}).get('_id', {})
        Notification.create_notification(
            owner_id=assigned_to,
            title=f'{story["story_id"]} - {story["title"]}',
            msg={
            "key": "assigned_to_notification",
            "message": {
                    "old": None,
                    "nuevo": None
            }
        },#"Has sido asignado a la historia",
            story=story,
            assigned_to=assigned_to,
            team_id=team_id
        )

    @staticmethod
    def create_creator_notification(story, team_id):
        Notification.create_notification(
            owner_id=ObjectId(story['creator']['_id']['$oid']),
            title=f'{story["story_id"]} - {story["title"]}',
            msg={
            "key": "creator_notification",
            "message": {
                    "old": None,
                    "nuevo": None
            }
        },#"Has creado la historia",
            story=story,
            assigned_to=None,
            team_id=team_id
        )

    @staticmethod
    def mark_notifications_as_viewed(user_id, team_id, filter_type):
        filter_criteria = {"team_id": ObjectId(team_id)}

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

        update_criteria = {
            "$push": {
                "viewed_by": {
                    "user_id": ObjectId(user_id),
                    "viewed": True
                }
            }
        }

        mongo_helper = MongoHelper()
        mongo_helper.astra.db['notifications'].update_many(
            {**filter_criteria, "viewed_by.user_id": {"$ne": ObjectId(user_id)}},
            update_criteria
        )

    @staticmethod
    def count_assigned_notifications(user_id, team_id):
        filter_criteria = {
            "user_id": ObjectId(user_id),
            "assigned_to": ObjectId(user_id),
            "team_id": ObjectId(team_id),  
            "viewed_by.user_id": {"$ne": ObjectId(user_id)}
        }
        return MongoHelper().count_documents(NOTIFICATIONS_COL, filter_criteria)

    @staticmethod
    def count_created_notifications(user_id, team_id):
        filter_criteria = {
            "user_id": ObjectId(user_id),
            "creator": ObjectId(user_id),
            "team_id": ObjectId(team_id), 
            "viewed_by.user_id": {"$ne": ObjectId(user_id)}
        }
        return MongoHelper().count_documents(NOTIFICATIONS_COL, filter_criteria)

    @staticmethod
    def count_subscribed_notifications(user_id, team_id):
        subscribed_story_ids = Notification.get_subscribed_story_ids(user_id, team_id)
        print("Subscribed Story IDs:", subscribed_story_ids)
        if not subscribed_story_ids:
            return 0

        try:
            subscribed_story_ids = [
                ObjectId(story_id['$oid']) for story_id in subscribed_story_ids if story_id and '$oid' in story_id
            ]
        except Exception as e:
            print(f"Error al convertir a ObjectId: {e}")
            return 0
        print("Segundas Subscribed Story IDs:", subscribed_story_ids)

        filter_criteria = {
            "user_id": ObjectId(user_id),
            "story_id.$oid": {"$in": [str(story_id) for story_id in subscribed_story_ids]}, 
            "viewed_by.user_id": {"$ne": ObjectId(user_id)}
        }
        print("Filter Criteria:", filter_criteria)
        try:
            count = MongoHelper().count_documents(NOTIFICATIONS_COL, filter_criteria)
        except Exception as e:
            print(f"Error al contar documentos: {e}")
            return 0
        print("count",count)
        return count

    @staticmethod
    def count_team_story_edits(user_id, team_id):
        filter_criteria = {
            "user_id": ObjectId(user_id),
            "team_id": ObjectId(team_id),
            "creator": {"$ne": ObjectId(user_id)}, 
            "assigned_to": {"$ne": ObjectId(user_id)},  
            "viewed_by.user_id": {"$ne": ObjectId(user_id)}
        }
        return MongoHelper().count_documents(NOTIFICATIONS_COL, filter_criteria)

    @staticmethod
    def get_subscribed_story_ids(user_id, team_id):
        user_id = ObjectId(user_id)
        team_id = ObjectId(team_id)

        filter_criteria = {
            "team": team_id,
        }
        all_stories = MongoHelper().get_documents_by(STORIES_COL, filter=filter_criteria)

        subscribed_stories = []
        for story in all_stories:
            if any(subscriber.get('$oid') == str(user_id) for subscriber in story.get('subscribers', [])):
                subscribed_stories.append(story)

        return [story.get('_id') for story in subscribed_stories]

def get_creator_notifications(user_id, team_id):
    filter_criteria = {
        "user_id": ObjectId(user_id),
        "creator": ObjectId(user_id),
        "team_id": ObjectId(team_id)  
    }
    return MongoHelper().get_documents_by(
        NOTIFICATIONS_COL, filter=filter_criteria, sort={'created_at': -1}
    )

def get_assigned_user_notifications(user_id, team_id):
    filter_criteria = {
        "user_id": ObjectId(user_id),
        "assigned_to": ObjectId(user_id),
        "team_id": ObjectId(team_id) 
    }
    return MongoHelper().get_documents_by(
        NOTIFICATIONS_COL, filter=filter_criteria, sort={'created_at': -1}
    )

def get_subscribed_notifications(user_id, team_id):
    notifications = MongoHelper().get_documents_by(
        NOTIFICATIONS_COL, {"user_id": ObjectId(user_id)}, sort=[('created_at', -1)]
    )
    subscribed_story_ids = Notification.get_subscribed_story_ids(user_id, team_id)

    filtered_notifications = [
        notification for notification in notifications
        if notification['story_id'] in subscribed_story_ids
    ]

    return filtered_notifications

def get_team_story_edits(team_id, user_id):
    filter_criteria = {
        "user_id": ObjectId(user_id),
        "team_id": ObjectId(team_id),
        "creator": {"$ne": ObjectId(user_id)}, 
        "assigned_to": {"$ne": ObjectId(user_id)}  
    }
    return MongoHelper().get_documents_by(NOTIFICATIONS_COL, filter=filter_criteria)
