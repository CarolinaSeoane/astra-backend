from enum import Enum
from bson import ObjectId

from app.db_connection import mongo
from app.utils import kanban_format, list_format
from app.services.mongoHelper import MongoHelper

class Type(Enum):
    BUGFIX = "Bugfix"
    FEATURE = "Feature"
    DISCOVERY = "Discovery"
    DEPLOYMENT = "Deployment"

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITIC = "Critic"

class Story:

    def __init__(self, title, description, acceptance_criteria, creator, assigned_to,
                 epic, sprint, estimation, tags, priority, attachments, comments,
                 story_type, tasks, related_stories, story_id, team, _id=ObjectId(),subscribers=None):
        self.title = title
        self.description = description
        self.acceptance_criteria = acceptance_criteria
        self.creator = creator
        self.assigned_to = assigned_to
        self.epic = epic
        self.sprint = sprint
        self.estimation = estimation
        self.tags = tags
        self.priority = priority
        self.attachments = attachments
        self.comments = comments
        self.story_type = story_type
        self.tasks = tasks
        self.related_stories = related_stories
        self._id = _id
        self.story_id = story_id
        self.estimation_method = estimation
        self.team = team
        self.subscribers = subscribers if subscribers is not None else []

    @classmethod
    def get_stories_by_team_id(cls, team_id: ObjectId, view_type, **kwargs):
        '''
        returns [] if no stories are found for the given team_id
        '''
        if view_type == 'kanban':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'estimation', 'tasks.title', 'tasks.status'}
        elif view_type == 'list':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'estimation', 'tasks.status', 'story_type', 'description'}
        else:
            projection = None

        filter = {
            "team": { "$eq": team_id },
        }

        # Add optional filters if provided in kwargs
        # for key, value in kwargs.items():
        #     print("%s == %s" % (key, value))

        if 'assigned_to' in kwargs and kwargs['assigned_to']:
            filter["assigned_to.username"] = kwargs['assigned_to']
        if 'sprint' in kwargs and kwargs['sprint']:
            filter["sprint.name"] = kwargs['sprint']
        if 'epic' in kwargs and kwargs['epic']:
            filter["epic.title"] = kwargs['epic']
        if 'priority' in kwargs and kwargs['priority']:
            filter["priority"] = kwargs['priority']
        if 'story_type' in kwargs and kwargs['story_type']:
            filter["story_type"] = kwargs['story_type']
        if 'story_id' in kwargs and kwargs['story_id']:
            filter["story_id"] = kwargs['story_id']

        stories = MongoHelper().get_documents_by('stories', filter=filter, projection=projection)
      
        if view_type == 'kanban':
            return kanban_format(stories)
        elif view_type == 'list':
            return list_format(stories)
        else:
            return stories

    @classmethod
    def get_story_fields(cls, sections=False):
        story_fields =  MongoHelper().get_documents_by('story_fields', sort={'order': 1})
        if sections:
            story_sections = {}
            for story_field in story_fields:
                sec = story_sections.setdefault(story_field["section"], [])
                sec.append(story_field)
            return story_sections
        return story_fields
    
    @classmethod
    def is_story_id_taken(cls, story_id):
        filter = {'story_id': story_id}
        return MongoHelper().document_exists("stories", filter)
    
    @classmethod
    def create_story(cls, story_document):
        return MongoHelper().create_document('stories', story_document)
    
    @classmethod
    def subscribe_to_story(cls, story_id: str, user_id: str):
        """
        Suscribe un usuario a una historia específica.
        """
        try:
            # Convertir IDs a ObjectId
            story_id = ObjectId(story_id)
            user_id = ObjectId(user_id)

            # Crear instancia de MongoHelper
            mongo_helper = MongoHelper()

            # Buscar la historia
            story = mongo_helper.get_document_by('stories', {'_id': story_id})
            if not story:
                return {"message": "Story not found", "status": 404}

            # Verificar si el usuario ya está suscrito
            if user_id in story.get('subscribers', []):
                return {"message": "User is already subscribed", "status": 400}

            # Agregar el user_id a la lista de suscriptores
            update = {"$addToSet": {"subscribers": user_id}}
            result = mongo_helper.update_collection('stories', {'_id': story_id}, update)

            if result.modified_count > 0:
                return {"message": "User successfully subscribed", "status": 200}
            else:
                return {"message": "Failed to subscribe", "status": 500}

        except Exception as e:
            print("Error subscribing to story:", e)
            return {"message": f"Failed to subscribe: {e}", "status": 500}
