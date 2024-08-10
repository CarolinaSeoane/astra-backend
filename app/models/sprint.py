from bson import ObjectId
from enum import Enum

from app.services.mongoHelper import MongoHelper

class SprintStatus(Enum):
    CURRENT = "Current"
    FINISHED = "Finished"
    FUTURE = "Future"
class Sprint:

    def __init__(self, name, sprint_number, quarter, year, start_date, end_date, status, target, team, _id=ObjectId()):
        self._id = _id
        self.name = name
        self.sprint_number: sprint_number
        self.quarter: quarter
        self.year: year
        self.start_date: start_date
        self.end_date: end_date
        self.status: status
        self.target: target
        self.team: team
    
    @classmethod
    def get_sprints(cls, team_id):
        '''
        returns None if the team has no sprints
        '''
        sort = {'start_date': 1}
        return MongoHelper().get_documents_by('sprints', {'team': ObjectId(team_id)}, sort)
