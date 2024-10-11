from app.models.team import Team
from app.services.astra_scheduler import generate_sprint_schedule

class Ceremony:

    def __init__(self, _id, name, start_date, google_meet_config, attendees):
        self._id = _id
        self.name = name
        self.start_date = start_date
        self.google_meet_config = google_meet_config
        self.attendees = attendees
        # google data

    def create_sprint_ceremonies(team_id):
        team_ceremonies_settings = Team.get_team_settings(team_id, 'ceremonies')['ceremonies']
        sprint_set_up = Team.get_team_settings(team_id, 'sprint_set_up')['sprint_set_up']
        generate_sprint_schedule(team_ceremonies_settings, sprint_set_up)
        
