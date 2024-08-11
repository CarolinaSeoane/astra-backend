from bson import ObjectId
from enum import Enum

from app.services.mongoHelper import MongoHelper

class SprintStatus(Enum):
    CURRENT = "Current"
    FINISHED = "Finished"
    FUTURE = "Future"
    ACTIVE = "Active" # Used for backlog
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
    def get_sprints(cls, team_id, quarter, year):
        '''
        returns None if the team has no sprints
        '''
        filter = {
            '$or': [
                {
                    'team': ObjectId(team_id),
                    'quarter': quarter, 
                    'year': year
                },
                {
                    'team': ObjectId(team_id),
                    'name': 'Backlog'
                },
            ]
        }
        sort = {'start_date': 1}
        documents = MongoHelper().get_documents_by('sprints', filter, sort)

        return documents[1:] + [documents[0]] # Send first element (backlog) to the back
