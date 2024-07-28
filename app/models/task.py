from enum import Enum


class Status(Enum):
    DOING = "Doing"
    NOT_STARTED = "Not Started"
    BLOCKED = "Blocked"
    DONE = "Done"


class Task:

    def __init__(self, _id, title, description, status, app):
        self._id = _id
        self.title = title
        self.description = description
        self.status = status
        self.app = app
