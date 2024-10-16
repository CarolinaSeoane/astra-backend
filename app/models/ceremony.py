from bson import ObjectId
from datetime import datetime

from app.models.team import Team
from app.services.astra_scheduler import generate_ceremonies_for_sprint
from app.models.sprint import Sprint
from app.services.mongoHelper import MongoHelper
from app.models.configurations import CollectionNames


CEREMONIES_COL = CollectionNames.CEREMONIES.value


class Ceremony:

    def __init__(self, _id, name, starts, google_meet_config, attendees, ceremony_type, ceremony_status):
        self._id = _id
        self.name = name
        self.starts = starts
        self.google_meet_config = google_meet_config
        self.attendees = attendees
        self.ceremony_type = ceremony_type
        self.ceremony_status = ceremony_status
        # google data

    @staticmethod
    def create_sprint_ceremonies(team_id, sprint):
        team_ceremonies_settings = Team.get_team_settings(team_id, 'ceremonies')['ceremonies']
        curr_sprint = Sprint.get_sprint_by({'_id': ObjectId(sprint)})
        ceremonies = generate_ceremonies_for_sprint(team_ceremonies_settings, curr_sprint)
        return MongoHelper().create_documents(CEREMONIES_COL, ceremonies)
    
    @staticmethod
    def get_sprint_ceremonies(sprint_id):
        filter = {'happens_on_sprint': ObjectId(sprint_id)}
        sort = {'starts': 1}
        return MongoHelper().get_documents_by(CEREMONIES_COL, filter = filter, sort = sort)

    @staticmethod
    def get_ceremonies_by_team_id(team_id, **kwargs):
        '''
        returns [] if no ceremonies are found for the given team_id
        '''
        filter = { "team": ObjectId(team_id) }
        sort = {'starts': 1}

        if 'sprint' in kwargs and kwargs['sprint']:
            filter["happens_on_sprint.name"] = kwargs['sprint']
        if 'ceremony_type' in kwargs and kwargs['ceremony_type']:
            filter["ceremony_type"] = kwargs['ceremony_type']
        if 'ceremony_status' in kwargs and kwargs['ceremony_status']:
            filter["ceremony_status"] = kwargs['ceremony_status']

        return MongoHelper().get_documents_by(CEREMONIES_COL, filter=filter, sort=sort)
    
    @staticmethod
    def get_upcoming_ceremonies_by_team_id(team_id, for_banner=True):
        '''
        returns [] if no ceremonies are found for the given team_id
        '''
        filter = { "team": ObjectId(team_id), "starts": {"$gt": datetime.today()} }
        sort = {'starts': 1}
        projection = {"ceremony_type", "starts", "ends", "google_meet_config.meetingUri"} if for_banner else {}
        return MongoHelper().get_documents_by(CEREMONIES_COL, filter=filter, sort=sort, projection=projection)

