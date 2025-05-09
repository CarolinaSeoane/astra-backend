from datetime import datetime
from bson import ObjectId
from dateutil import parser

from app.services.mongoHelper import MongoHelper
from app.models.configurations import SprintStatus, CollectionNames
from app.utils import list_format, mongo_query

SPRINTS_COL = CollectionNames.SPRINTS.value
STORIES_COL = CollectionNames.STORIES.value


class Sprint:

    def __init__(
            self, name, sprint_number, quarter, year, start_date,
            end_date, status, target, team, completed, actual_end_date, _id=ObjectId()
        ):
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
    def get_sprints(team_id, year, future=False, backlog=True, all_from_year=False):
        '''
        returns None if the team has no sprints
        '''
        filter = {}

        if all_from_year:
            filter = {
                '$or': [
                    {
                       'team': ObjectId(team_id),
                        'year': year
                    },
                ]
            }
        elif future:
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
                ]
            }
        else:
            filter = {
                '$or': [
                    {
                        'team': ObjectId(team_id),
                        'status': { "$ne": SprintStatus.FUTURE.value},
                        'name': { "$ne": "Backlog" }
                    },
                ]
            }
            if year:
                filter['$or'][0]['year'] = year

        if backlog:
            filter['$or'].append({
                'team': ObjectId(team_id),
                'name': 'Backlog'
            })

        sort = {'start_date': 1}
        documents = MongoHelper().get_documents_by(SPRINTS_COL, filter, sort)

        if not documents:
            return None

        if backlog:
            return documents[1:] + [documents[0]] # Send first element (backlog) to the back
        return documents

    @staticmethod
    def get_all_sprints(team_id):
        filter = {'team': ObjectId(team_id), 'name': {'$ne': 'Backlog'}}
        sort = {'start_date': -1}
        return MongoHelper().get_documents_by(SPRINTS_COL, filter, sort)

    @staticmethod
    def get_velocity(team_id, sprint_name):
        sprint = Sprint.get_sprint_by({
            "name": sprint_name,
            "team": team_id
        })
        filter = {
            "team": team_id,
            "name": { "$ne": "Backlog" },
            "start_date": { "$lte": datetime.strptime(sprint["start_date"]["$date"], '%Y-%m-%dT%H:%M:%S%z') }
        }
        sort = {'start_date': 1}
        projection = {"name", "target", "completed"}
        return MongoHelper().get_documents_by(
            SPRINTS_COL, filter=filter, sort=sort, projection=projection
        )

    @staticmethod
    def create_backlog_for_new_team(team_id):
        new_backlog = {
            "name": 'Backlog',
            "status": SprintStatus.ACTIVE.value,
            "team": team_id
        }
        return MongoHelper().create_document(SPRINTS_COL, new_backlog)

    @staticmethod
    def get_target_points(sprint, team_id):
        filter = {
            "name": sprint,
            "team": ObjectId(team_id)
        }
        projection = {"target": 1, "_id": 0}
        return MongoHelper().get_document_by(SPRINTS_COL, filter, projection=projection).get("target", 0)

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

        cursor = MongoHelper().aggregate(STORIES_COL, match, group, project=projection)
        cursor_list = list(cursor)
        if isinstance(cursor_list, list) and len(cursor_list) > 0:
            target_dict = cursor_list[0]
            if "target" in target_dict:
                return target_dict["target"]
        return 0

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

        completed_points = Sprint.get_completed_points_up_to(
            sprint['name'], sprint['team']['$oid'], datetime.today()
        )

        if completed_points:
            total_sps_finished = completed_points[0]['completed_points']
        else:
            total_sps_finished = 0

        # Set final SP completed
        # Set status as finished
        filter = {'_id': ObjectId(sprint_id)}
        update = {
            '$set': {
                'status': SprintStatus.FINISHED.value,
                'completed': total_sps_finished,
                'actual_end_date': datetime.today()
            }
        }
        return MongoHelper().update_document(SPRINTS_COL, filter, update)

    @staticmethod
    def start_sprint(sprint_id):
        '''
        Starts a sprint by setting the status of the given sprint as CURRENT and
        deleting the next attribute from the doc. This also sets the target points
        '''
        # Get target points
        target = 0
        match = {'sprint._id': ObjectId(sprint_id)}
        group = {'_id': None, 'target': {'$sum': '$estimation'}}
        target_cursor = MongoHelper().aggregate(STORIES_COL, match, group)
        for t in target_cursor:
            target = t.get("target", 0)

        # Set status as current and delete next flag
        filter = {'_id': ObjectId(sprint_id)}
        update = {
            '$set': {
                'status': SprintStatus.CURRENT.value,
                'actual_start_date': datetime.today(),
                'target': target,
            },
            '$unset': {'next': ""}
        }
        return MongoHelper().update_document(SPRINTS_COL, filter, update)

    @staticmethod
    def set_following_sprint(team_id):
        '''
        Adds the next attribute to the first sprint found with a FUTURE status.
        '''
        # curr_sprint = Sprint.get_sprint_by({'_id': ObjectId(sprint_id)})

        # Find the next sprint
        filter = {'team': ObjectId(team_id), 'status': SprintStatus.FUTURE.value}
        sort = {'start_date': 1}
        next_sprint = MongoHelper().get_document_by(SPRINTS_COL, filter, sort)

        # Set next flag
        if next_sprint:
            filter = {'_id': ObjectId(next_sprint['_id']['$oid'])}
            update = {'$set': {'next': True}}
            MongoHelper().update_document(SPRINTS_COL, filter, update)

    @staticmethod
    def there_is_a_next_sprint(team_id):
        '''
        Checks if there is a sprint with the flag "next"
        '''
        # Find a sprint with the next flag
        filter = {'team': ObjectId(team_id), 'next': {'$exists': True}}
        return  MongoHelper().get_document_by(SPRINTS_COL, filter)

    @staticmethod
    @mongo_query
    def add_completed_points(sprint, team_id, points):
        match = {
            "name": sprint,
            "team": ObjectId(team_id),
        }
        update = { "$inc": {"completed": points} }
        return MongoHelper().update_document(SPRINTS_COL, match, update)

    @staticmethod
    def get_active_sprints(team_id):
        '''
        Returns active sprints (Finished and Current) for a given team. Excludes the Backlog sprint.
        '''
        filter = {
            'team': ObjectId(team_id),
            '$or': [
                {'status': SprintStatus.CURRENT.value},
                {'status': SprintStatus.FINISHED.value}
            ]
        }
        sort_criteria = [('start_date', 1)]  # 1 for ascending, -1 for descending
        documents = MongoHelper().get_documents_by('sprints', filter,  sort=sort_criteria)
        return documents if documents else None

    @staticmethod
    def get_sprints_past(team_id):
        '''
        Returns only Finished sprints for a given team. Excludes the Backlog sprint.
        '''
        filter = {
            'team': ObjectId(team_id),
            'status': SprintStatus.FINISHED.value
        }
        documents = MongoHelper().get_documents_by('sprints', filter)
        return documents if documents else None

    @staticmethod
    def count_stories(sprint_id, team_id, user_id):
        '''
        Returns the total stories told and the number of stories not completed in
        a sprint for a team and a specific user.
        '''
        filter_sprint = {
            '_id': ObjectId(sprint_id)
        }
        #print("id filter sprint", filter_sprint)

        sprint_documents = MongoHelper().get_documents_by('sprints', filter_sprint)
        #print("sprint_documents", sprint_documents

        if not sprint_documents:
            return 0, 0

        sprint = sprint_documents[0]

        try:
            sprint_start_date_str = sprint['start_date']['$date']
            sprint_end_date_str = sprint['end_date']['$date']

            sprint_start_date = datetime.strptime(sprint_start_date_str, "%Y-%m-%dT%M:%S:%fZ")
            sprint_end_date = datetime.strptime(sprint_end_date_str, "%Y-%m-%dT%M:%S:%fZ")
        except (KeyError, ValueError):
            return 0, 0

        filter_stories = {
            'team': ObjectId(team_id),
            'assigned_to._id': ObjectId(user_id),
            'sprint._id': ObjectId(sprint_id)
        }

        stories = MongoHelper().get_documents_by('stories', filter_stories)

        if not stories:
            return 0, 0

        stories= list_format(stories) #Format List add COMPLETENESS

        total_stories = 0
        incomplete_stories = 0

        for story in stories:
            total_stories += 1

            story_end_date_dict = story.get('end_date', None)

            if story_end_date_dict and '$date' in story_end_date_dict:
                story_end_date_str = story_end_date_dict['$date']

                # Convert parser.isoparse
                if story_end_date_str:
                    story_end_date = parser.isoparse(story_end_date_str).replace(tzinfo=None)
                    #print("story_end_date", story_end_date)
                else:
                    story_end_date = None
            else:
                story_end_date = None

            completeness = story.get('completeness', 0)

            if completeness < 100 or not story_end_date or story_end_date > sprint_end_date:
                incomplete_stories += 1

        #print(f"TOTAL STORIES: {total_stories}, Incomplete Stories: {incomplete_stories}")

        return total_stories, incomplete_stories

    @staticmethod
    def get_latest_sprint(team_id):
        '''
        Returns None if the team only has a backlog but no sprints
        '''
        filter = {'team': ObjectId(team_id), 'start_date': { '$exists': True }}
        sort = {'start_date': -1}
        return MongoHelper().get_document_by(SPRINTS_COL, filter, sort)

    @staticmethod
    def get_stories_grouped_by_status(sprint_name, team_id):
        match = {
            "sprint.name": sprint_name,
            "team": ObjectId(team_id)
        }
        group = {
            "_id": "$tasks.status",
            "value": { "$sum": 1 }
        }
        unwind = "$tasks"
        return MongoHelper().aggregate(STORIES_COL, match=match, group=group, unwind=unwind)

    @staticmethod
    def add_sprints(sprints):
        return MongoHelper().create_documents(SPRINTS_COL, sprints)

    @staticmethod
    def get_total_stories_count(sprint_name, team_id):
        match = {
            "sprint.name": sprint_name,
            "team": team_id
        }
        return len(MongoHelper().get_documents_by(STORIES_COL, match))

    @staticmethod
    def get_future_sprints(team_id):
        '''
        Returns future sprints (Future and Current) for a given team. Excludes the Backlog sprint.
        '''
        filter = {
            'team': ObjectId(team_id),
            '$or': [
                {'status': SprintStatus.CURRENT.value},
                {'status': SprintStatus.FUTURE.value}
            ]
        }

        documents = MongoHelper().get_documents_by(SPRINTS_COL, filter)
        return documents if documents else None

    @staticmethod
    def get_current_sprint(team_id):
        '''
        Returns current sprint for a given team. Excludes the Backlog sprint.
        '''
        match = {
            'team': ObjectId(team_id),
            'status': SprintStatus.CURRENT.value,
        }

        documents = MongoHelper().get_document_by(SPRINTS_COL, match)
        return documents if documents else None


    @staticmethod
    def set_points_current_sprint(sprint_id):
        '''
        set_points_current_sprint in planning board
        '''
        # Get target points
        target = 0
        match = {'sprint._id': ObjectId(sprint_id)}
        group = {'_id': None, 'target': {'$sum': '$estimation'}}
        target_cursor = MongoHelper().aggregate(STORIES_COL, match, group)


        for t in target_cursor:
            target = t.get("target", 0)



        #print("target total de puntos:", target )

        
        # Set status as current and delete next flag
        filter = {'_id': ObjectId(sprint_id)}
        update = {
            '$set': {
            #    'status': SprintStatus.CURRENT.value,
            #    'actual_start_date': datetime.today(),
                'target': target,
            },

        }
        respuesta = MongoHelper().update_document(SPRINTS_COL, filter, update)
        ''
        if respuesta.modified_count > 0:
            print("modificado")# Update successful
        else:
            print("no modificado")  # Update failed
        ''
        return target