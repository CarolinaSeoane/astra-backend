from bson import ObjectId

from app.utils import kanban_format, list_format
from app.services.mongoHelper import MongoHelper
from app.models.configurations import Configurations, CollectionNames


STORIES_COL = CollectionNames.STORIES.value


class Story:

    def __init__(self, title, description, acceptance_criteria, creator, assigned_to,
                 epic, sprint, estimation, tags, priority, attachments, comments,
                 story_type, tasks, related_stories, story_id, team, _id=ObjectId()):
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

    @staticmethod
    def get_stories_by_team_id(team_id: ObjectId, view_type, **kwargs):
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

        stories = MongoHelper().get_documents_by(STORIES_COL, filter=filter, projection=projection)
      
        if view_type == 'kanban':
            return kanban_format(stories)
        elif view_type == 'list':
            return list_format(stories)
        else:
            return stories

    @staticmethod
    def get_story_fields(sections=False):
        story_fields = Configurations.get_all_possible_story_fields()['story_fields']
        if sections:
            story_sections = {}
            for story_field in story_fields:
                sec = story_sections.setdefault(story_field["section"], [])
                sec.append(story_field)
            return story_sections
        return story_fields
    
    @staticmethod
    def is_story_id_taken(story_id):
        filter = {'story_id': story_id}
        return MongoHelper().document_exists(STORIES_COL, filter)
    
    @staticmethod
    def create_story(story_document):
        return MongoHelper().create_document(STORIES_COL, story_document)
    
    @staticmethod
    def get_done_story_points_count_by_day(story_id, team_id):
        match = {
            "sprint.name": story_id,
            "team": ObjectId(team_id)
        }
        group = {
            "_id": "$end_date",
            "completed_points": { "$sum": "$estimation" }
        }
        sort = {"_id": 1}   # because the sorting occurs after the group by, we no longer have the end_date field. that data
                            # is now at _id. renaming of the resulting group by fields is possible is really needed.
        return MongoHelper().aggregate(STORIES_COL, match, group, sort)
