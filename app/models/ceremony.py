from datetime import datetime, timedelta
from bson import ObjectId

from app.models.team import Team
from app.services.astra_scheduler import generate_ceremonies_for_sprint
from app.models.sprint import Sprint
from app.services.mongoHelper import MongoHelper
from app.models.configurations import CollectionNames, GoogleMeetDataStatus
from app.services.google_meet import list_conference_records, list_conference_record_participants


CEREMONIES_COL = CollectionNames.CEREMONIES.value
BOARDS_COL = CollectionNames.BOARDS.value


class Ceremony:

    def __init__(self, _id, name, starts, google_meet_config,
                 attendees, ceremony_type, ceremony_status):
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
        if 'ceremony_id' in kwargs and kwargs['ceremony_id']:
            filter["_id"] = kwargs['ceremony_id']
        return MongoHelper().get_documents_by(CEREMONIES_COL, filter=filter, sort=sort)

    @staticmethod
    def get_upcoming_ceremonies_by_team_id(team_id, for_banner=True):
        '''
        returns [] if no ceremonies are found for the given team_id
        '''
        filter = { "team": ObjectId(team_id), "starts": {"$gt": datetime.today()} }
        sort = {'starts': 1}  
        projection = (
            {"_id", "ceremony_type", "starts", "ends", "google_meet_config.meetingUri"}
            if for_banner
            else {}
        )
        return MongoHelper().get_documents_by(
            CEREMONIES_COL, filter=filter, sort=sort, projection=projection
        )
    
    @staticmethod
    def get_google_meet_data(user, ceremony):
        conference_records = list_conference_records(user.access_token, user.refresh_token, ceremony)
        if not conference_records:
            # Set attendees and transcript as Unavailable
            participants, transcript = GoogleMeetDataStatus.UNAVAILABLE.value, GoogleMeetDataStatus.UNAVAILABLE.value
            MongoHelper().update_document(
                CEREMONIES_COL,
                filter={'_id': ObjectId(ceremony['_id']['$oid'])},
                update={'$set': {'attendees': participants, 'transcript': transcript}}
            )

        else:
            # I'll only consider the first conference record. If more than one record was found for the duration of the meeting, only the
            # first will be recorded as the meeting

            # Fetch participants from google service
            conference_record = conference_records['conferenceRecords'][0]
            participants = list_conference_record_participants(user.access_token, user.refresh_token, conference_record['name'])['participants']

            # TODO: Fetch transcript from google service    

            # Update record
            MongoHelper().update_document(
                CEREMONIES_COL,
                filter={'_id': ObjectId(ceremony['_id']['$oid'])},
                update={'$set': {'attendees': participants, 'transcript': ''}}
            )

        return {'attendees': participants, 'transcript': ''}

    @staticmethod
    def get_current_ceremony_by_team_id(team_id):
        '''
        Returns the current ceremony for the given team_id,
        or None if no current ceremony is found.
        '''
        current_time = datetime.now()
        filter = {
            "team": ObjectId(team_id),
            "starts": {"$lte": current_time}, 
            "ends": {"$gte": current_time}   
        }

        current_ceremony = MongoHelper().get_documents_by(
            CEREMONIES_COL,
            filter=filter,
            sort={"starts": 1}
        )

        return current_ceremony[0] if current_ceremony else None

    @staticmethod
    def get_ceremony_by_id(ceremony_id):
        if not ObjectId.is_valid(ceremony_id):
            return None

        return MongoHelper().get_document_by(CEREMONIES_COL, {'_id': ObjectId(ceremony_id)})

    @staticmethod
    def save_board(team_id, ceremony_id, board_state):
        new_board = {
            "team_id": team_id,
            "ceremony_id": ceremony_id,
            "board_state": board_state,
            "saved_at": datetime.utcnow()
        }
        MongoHelper().create_document(BOARDS_COL, new_board)

    @staticmethod
    def get_ceremony_date(ceremony_id):
        """Obtiene la fecha de la ceremonia especificada por su ID y retorna el día anterior."""
        ceremony = Ceremony.get_ceremony_by_id(ceremony_id)

        print(f"Ceremony data: {ceremony}")
        if not ceremony:
            print("Error: No se encontró la ceremonia con el ID proporcionado.")
            return None

        if 'ends' not in ceremony or not ceremony['ends']:
            print("Error: No se encontró la fecha de fin ('ends') en la ceremonia.")
            return None

        if isinstance(ceremony['ends'], dict) and '$date' in ceremony['ends']:
            ends_date_str = ceremony['ends']['$date']
            ceremony_date = datetime.fromisoformat(ends_date_str[:-1]) - timedelta(days=1)
            print(f"Using ceremony date for filtering: {ceremony_date}")
            return ceremony_date
        print("Error: 'ends' no es un dict o no contiene '$date'.")
        return None

    @staticmethod
    def is_ceremony_active(ceremony_id):
        ceremony = Ceremony.get_ceremony_by_id(ceremony_id)
        if not ceremony:
            return False

        starts = ceremony.get('starts')
        ends = ceremony.get('ends')

        if isinstance(starts, dict) and '$date' in starts:
            starts = starts['$date']
        if isinstance(ends, dict) and '$date' in ends:
            ends = ends['$date']

        if isinstance(starts, str):
            starts = datetime.fromisoformat(starts)
        elif isinstance(starts, int):
            starts = datetime.fromtimestamp(starts)

        if isinstance(ends, str):
            ends = datetime.fromisoformat(ends)
        elif isinstance(ends, int):
            ends = datetime.fromtimestamp(ends)

        if starts.tzinfo is not None:
            starts = starts.replace(tzinfo=None)
        if ends.tzinfo is not None:
            ends = ends.replace(tzinfo=None)

        return starts <= datetime.now() <= ends
