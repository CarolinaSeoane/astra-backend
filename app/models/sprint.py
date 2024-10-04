from bson import ObjectId
import datetime

from app.services.mongoHelper import MongoHelper
from app.models.configurations import SprintStatus, CollectionNames


SPRINTS_COL = CollectionNames.SPRINTS.value
STORIES_COL = CollectionNames.STORIES.value


class Sprint:

    def __init__(self, name, sprint_number, quarter, year, start_date, end_date, status, target, team, completed, actual_end_date, _id=ObjectId()):
        self._id = _id
        self.name = name
        self.sprint_number = sprint_number
        self.quarter = quarter
        self.year = year
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.target = target
        self.team = team
        self.completed = completed
        self.actual_end_date = actual_end_date

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
        documents = MongoHelper().get_documents_by(SPRINTS_COL, filter, sort)

        if not documents:
            return None
        return documents[1:] + [documents[0]] # Send first element (backlog) to the back

    @staticmethod
    def get_all_sprints(team_id):
        filter = {'team': ObjectId(team_id), 'name': {'$ne': 'Backlog'}}
        sort = {'start_date': -1}
        return MongoHelper().get_documents_by(SPRINTS_COL, filter, sort)

    @staticmethod
    def get_velocity(team_id):
        filter = {
            "team": { "$eq": team_id },
            "name": { "$ne": "Backlog" }
        }
        sort = {'sprint_number': 1}
        projection = {"name", "target", "completed"}
        return MongoHelper().get_documents_by(SPRINTS_COL, filter=filter, sort=sort, projection=projection)

    @staticmethod
    def create_backlog_for_new_team(team_id):
        new_backlog = {
            "name": 'Backlog',
            "status": SprintStatus.ACTIVE.value,
            "team": team_id
        }
        return MongoHelper().add_new_element_to_collection(SPRINTS_COL, new_backlog)

    @staticmethod
    def get_target_points(sprint, team_id):
        filter = {
            "name": sprint,
            "team": ObjectId(team_id)
        }
        projection = {"target": 1, "_id": 0}
        return MongoHelper().get_document_by(SPRINTS_COL, filter, projection=projection)["target"]

    @staticmethod
    def get_start_and_end_dates(sprint, team_id):
        filter = {
            "name": sprint,
            "team": ObjectId(team_id)
        }
        projection = {"start_date", "end_date"}
        return MongoHelper().get_document_by(SPRINTS_COL, filter, projection=projection)

    @staticmethod
    def get_completed_points_up_to(sprint, team_id, date):
        match = {
            "sprint.name": sprint,
            "team": ObjectId(team_id),
            "end_date": { "$lte": date }
        }
        group = {
            "_id": "$name",
            "completed_points": { "$sum": "$estimation" }
        }
        # sort = {"_id": 1}  # Sort by _id (which is end_date after grouping)
        projection = {"_id": 0}

        return list(MongoHelper().aggregate(STORIES_COL, match, group, project=projection))

    @staticmethod
    def get_commited_points_up_to(sprint, team_id, date):
        match = {
            "sprint.name": sprint,
            "team": ObjectId(team_id),
            "added_to_sprint": { "$lte": date }
        }
        group = {
            "_id": "$sprint.name",
            "target": { "$sum": "$estimation" }
        }
        # sort = {"_id": 1}  # Sort by _id (which is end_date after grouping)
        projection = {"_id": 0}

        return list(MongoHelper().aggregate(
            STORIES_COL, match, group, project=projection
            ))[0]["target"]

    @staticmethod
    def get_sprint_by(filter):
        '''
        returns None if sprint is not found and dict if found
        '''
        return MongoHelper().get_document_by(SPRINTS_COL, filter)
    
    @staticmethod
    def finish_sprint(sprint_id):
        '''
        Finishes a sprint by setting status of the given sprint as FINISHED
        and adding a total count of the finished story points
        '''
        # Get finished SPs sum
        sprint = Sprint.get_sprint_by({'_id': ObjectId(sprint_id)})
        total_sps_finished = Sprint.get_completed_points_up_to(sprint['name'], sprint['team']['$oid'], datetime.datetime.today())[0]['completed_points']

        # Set final SP completed
        # Set status as finished
        filter = {'_id': ObjectId(sprint_id)}
        update = {'$set': {'status': SprintStatus.FINISHED.value, 'completed': total_sps_finished, 'actual_end_date': datetime.datetime.today()}}
        return MongoHelper().update_document(SPRINTS_COL, filter, update)
