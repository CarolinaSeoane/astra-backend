from datetime import datetime
from bson import ObjectId

from app.models.sprint import Sprint
from app.models.task import Task
from app.utils import kanban_format, list_format, mongo_query
from app.utils import kanban_format, list_format, list_format_with_task_details
from app.services.mongoHelper import MongoHelper
from app.models.configurations import Configurations, CollectionNames, Status
from app.db_connection import mongo

STORIES_COL = CollectionNames.STORIES.value
DONE_STATUS = Status.DONE.value


class Story:

    def __init__(self, title, description, acceptance_criteria, creator, assigned_to,
                 epic, sprint, estimation, tags, priority, attachments, comments, story_type,
                 tasks, related_stories, story_id, team, _id=ObjectId(), subscribers=None):
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

    @staticmethod
    def get_stories_by_team_id(team_id: ObjectId, view_type, **kwargs):
        '''
        returns [] if no stories are found for the given team_id
        '''
        if view_type == 'kanban':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'estimation', 'tasks.title', 'tasks.status'}
        elif view_type == 'list':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'estimation', 'tasks.status', 'story_type', 'description', 'epic.title'}
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
        if 'story_status' in kwargs and kwargs['story_status']:
            filter["story_status"] = kwargs['story_status']

        stories = MongoHelper().get_documents_by(STORIES_COL, filter=filter, projection=projection)

        if view_type == 'kanban':
            return kanban_format(stories)
        elif view_type == 'list':
            return list_format(stories)
        else:
            return stories
    
    @staticmethod
    def get_standup_stories(team_id: ObjectId, view_type, **kwargs):
        '''
        Returns [] if no stories are found for the given team_id
        '''
        print("Ceremony date being passed to filter:",kwargs.get('ceremony_date'))
        if view_type == 'kanban':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'estimation', 'tasks.title', 'tasks.status', 'creation_date'}
        elif view_type == 'list':
            projection = {'_id', 'story_id', 'title', 'assigned_to', 'estimation', 'tasks.status', 'story_type', 'description', 'creation_date'}
        else:
            projection = None

        filter = {
            "team": {"$eq": team_id},
        }

        
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
        if 'story_status' in kwargs and kwargs['story_status']:
            filter["story_status"] = kwargs['story_status']
        
        if 'ceremony_date' in kwargs and kwargs['ceremony_date']:
            
            filter["creation_date"] = {"$lt": kwargs['ceremony_date']}

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
    def get_story_by_id(story_id):
        return MongoHelper().get_document_by(STORIES_COL, filter={"story_id": story_id})

    @staticmethod
    def is_done(story):
        return Task.get_story_status(story["tasks"]) == DONE_STATUS

    @staticmethod
    def finalize_story(story, team_id):
        if "end_date" not in story:
            sprint_name = story["sprint"]["name"]
            points = story["estimation"]
            story["end_date"] = datetime.combine(datetime.now().date(), datetime.min.time())
            Sprint.add_completed_points(sprint_name, team_id, points)
        return Story.update(story, new_status=DONE_STATUS)

    @staticmethod
    def update(story, new_status):
        story["story_status"] = new_status
        match = {'story_id': story["story_id"]}
        return MongoHelper().replace_document(STORIES_COL, match, new_document=story)

    @staticmethod
    @mongo_query
    def subscribe_to_story(story_id, user_id):
        mongo_helper = MongoHelper()

        story = mongo_helper.get_document_by(STORIES_COL, {'story_id': story_id})
        if not story:
            return {"message": "Story not found", "status": 404}

        if {"$oid": user_id} in story.get('subscribers', []):
            return {"message": "User is already subscribed", "status": 200}

        user_id = ObjectId(user_id)
        update = {"$addToSet": {"subscribers": user_id}}
        mongo_helper.update_collection(STORIES_COL, {'story_id': story_id}, update)
        return {"message": "You have been successfully subscribed", "status": 200}

    @staticmethod
    @mongo_query
    def unsubscribe_to_story(story_id, user_id):
        mongo_helper = MongoHelper()
        story = mongo_helper.get_document_by(STORIES_COL, {"story_id": story_id})
        if story:
            updated_subscribers = [
                sub for sub in story.get("subscribers", []) if sub["$oid"] != user_id
            ]
            MongoHelper().update_collection(
                collection_name=STORIES_COL,
                filter={"story_id": story_id},
                update={"$set": {"subscribers": updated_subscribers}}
                # update={"$pull": {"subscribers": {"$oid": user_id}}}
            )
            return {
                "message": ["You have been successfully unsubscribed from story"],
                "status": 200
            }

    @staticmethod
    def delete(team_id, story_id):
        match = {
            "team": ObjectId(team_id),
            "story_id": story_id
        }
        return MongoHelper().delete_element_from_collection(STORIES_COL, match)
  

    @staticmethod
    def get_list_stories_in_team_id_by_sprint_current_and_selected(team_id, sprint_current, sprint_selected):
        '''
        Returns all stories for the given team_id and sprint_name in list format.
        If no stories are found, returns an empty list.
        '''
        #print("sprint.name", sprint)
        '''
        filter = {
        'team': ObjectId(team_id),  # Convert ObjectId to string for comparison
        'sprint.name': sprint          # Directly use the sprint name
        }
        '''
        filter = {
            'team': ObjectId(team_id),
            'sprint.name': {'$in': [sprint_selected, sprint_current, "Backlog"]}
        }

        stories = MongoHelper().get_documents_by(STORIES_COL, filter=filter)
        #print("stories", stories)
        listado = list_format_with_task_details(stories)
        #print("listado", listado)
        return listado


             
    @staticmethod
    def put_new_status_and_new_sprint_to_story(team_id, story_id, new_sprint_name):
        '''
        new sprint
        '''
        #print("team_id.name", team_id)
        #print("story_id.name", story_id)
        #print("new_sprint_name.name", new_sprint_name)

        #Sprint.get_sprint_by()
        res_sprint = Sprint.get_sprint_by({
            "name": new_sprint_name,
            "team": ObjectId(team_id)
        })

        #print("rest sprint", res_sprint)

        sprint_id = res_sprint["_id"]["$oid"]

        #print("Sprint ID:", sprint_id)
        
        result = mongo.db.stories.update_one(
            {
                'story_id': story_id,
                'team': ObjectId(team_id)
            },
            {
                '$set': {
                    #'story_status': new_status,
                    'sprint': {
                        '_id': ObjectId(sprint_id),  # Guardamos el ObjectId directamente
                        'name': new_sprint_name
                    }
                }
            }
        )
        #print("result mongo",  result)
       
        if result.modified_count > 0:
            return True
        else:
            return False
