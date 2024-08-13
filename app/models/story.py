from enum import Enum
from bson import ObjectId, json_util
import json

from app.db_connection import mongo
from app.utils import kanban_format, list_format
from app.services.mongoHelper import MongoHelper

class Type(Enum):
    BUGFIX = "Bugfix"
    FEATURE = "Feature"
    DISCOVERY = "Discovery"
    DEPLOYMENT = "Deployments"

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITIC = "Critic"

class Story:

    def __init__(self, title, description, acceptance_criteria, creator, assigned_to,
                 epic, sprint, estimation, tags, priority, attachments, comments,
                 type, tasks, related_stories, story_id, team, _id=ObjectId()):
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
        self.type = type
        self.tasks = tasks
        self.related_stories = related_stories
        self._id = _id
        self.story_id = story_id
        self.estimation_method = estimation
        self.team = team

    @classmethod
    def get_stories_by_team_id(cls, team_id: ObjectId, view_type, **kwargs):
        '''
        returns [] if no stories are found for the given team_id
        '''
        if view_type == 'kanban':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'estimation', 'tasks.title', 'tasks.status'}          
        elif view_type == 'list':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'estimation', 'tasks.status', 'type', 'description'}          
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
        if 'type' in kwargs and kwargs['type']:
            filter["type"] = kwargs['type']

        stories_list = list(mongo.db.stories.find(filter = filter, projection = projection))
        response = json_util.dumps(stories_list) # mongoDb doc to JSON-encoded string.
        stories = json.loads(response) # JSON-encoded string to Python list of dictionaries.
        
        if view_type == 'kanban':
            return kanban_format(stories)
        elif view_type == 'list':
            return list_format(stories)
        else:
            return stories

    @classmethod
    def get_story_fields(cls):
        # return MongoHelper().get_collection('story_fields')
        pipeline = [
            {
                '$group': {
                    'section': '$section',
                    'data': '$value'
                }
            }
        ]
        return MongoHelper().get_documents_grouped_by('story_fields', pipeline)