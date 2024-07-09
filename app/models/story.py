from enum import Enum


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
                 type, tasks, related_stories, _id, story_id, estimation):
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
