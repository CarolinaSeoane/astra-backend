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
    
    @staticmethod
    def get_sprints(team_id, quarter, year, future):
        '''
        returns None if the team has no sprints
        '''
        filter = {}
        
        if future:
            filter = {
                '$or': [
                    {
                        'team': ObjectId(team_id),
                        'status': SprintStatus.CURRENT.value
                    },
                    {
                        'team': ObjectId(team_id),
                        'status': SprintStatus.FUTURE.value
                    },
                    {
                        'team': ObjectId(team_id),
                        'name': 'Backlog'
                    },
                ]
            }
        else:
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

        if not documents:
            return None
        return documents[1:] + [documents[0]] # Send first element (backlog) to the back

    @classmethod
    def get_velocity(cls, team_id):
        filter = {
            "team": { "$eq": team_id },
            "name": { "$ne": "Backlog" }
        }
        sort = {'sprint_number': 1}
        projection = {"name", "target", "completed"}
        return MongoHelper().get_documents_by("sprints", filter=filter, sort=sort, projection=projection)
    
    @staticmethod
    def create_backlog_for_new_team(team_id):
        new_backlog = {
            "name": 'Backlog',
            "status": SprintStatus.ACTIVE.value,
            "team": team_id
        }
        return MongoHelper().add_new_element_to_collection('sprints', new_backlog)
