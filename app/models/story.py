from enum import Enum
from bson import ObjectId, json_util
import json

from app.db_connection import mongo
from app.utils import kanban_format

class Type(Enum):
    BUGFIX = "Bugfix"
    FEATURE = "Featue"
    DISCOVERY = "Discovery"
    DEPLOYMENT = "Deployments"

class Type(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITIC = "Critic"

class Story:

    def __init__(self, title, description, acceptance_criteria, creator, assigned_to,
                 epic, sprint, story_points, tags, priority, attachments, comments,
                 type, tasks, related_stories, story_id, estimation, team, _id=ObjectId()):
        self.title = title
        self.description = description
        self.acceptance_criteria = acceptance_criteria
        self.creator = creator
        self.assigned_to = assigned_to
        self.epic = epic
        self.sprint = sprint
        self.story_points = story_points
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
    def get_stories_by_team_id(cls, team_id: ObjectId, view_type):
        '''
        returns [] if no stories are found for the given team_id
        '''
        if view_type == 'kanban':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'story_points', 'tasks.title', 'tasks.status'}          
        else:
            projection = None

        filter = {
            "team": { "$eq": team_id },
        }

        stories_list = list(mongo.db.stories.find(filter = filter, projection = projection))
        response = json_util.dumps(stories_list) # mongoDb doc to JSON-encoded string.
        stories = json.loads(response) # JSON-encoded string to Python list of dictionaries.
        
        if view_type == 'kanban':
            return kanban_format(stories)
        else:
            return stories

    