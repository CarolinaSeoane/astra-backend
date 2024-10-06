from datetime import datetime, timedelta, time

from app.models.team import Team
from app.utils import get_weekday_number, get_next_weekday
from app.models.configurations import CeremonyStartOptions, CeremonyType, CeremonyStatus


class Ceremony:

    def __init__(self, _id, name, start_date, google_meet_config, attendees):
        self._id = _id
        self.name = name
        self.start_date = start_date
        self.google_meet_config = google_meet_config
        self.attendees = attendees
        # google data

    def create_sprint_ceremonies(team_id):
        team_ceremonies_settings = Team.get_team_settings(team_id, 'ceremonies')
        sprint_set_up = Team.get_team_settings(team_id, 'sprint_set_up')['sprint_set_up']
        generate_sprint_schedule(team_ceremonies_settings, sprint_set_up)
        

# def generate_sprint_schedule(ceremonies, sprint_set_up, sprint_start_date=None):
def generate_sprint_schedule(team_ceremonies_settings, sprint_set_up, sprint_start_date=None):
        schedule = []

        # Determine sprint start date
        if sprint_start_date:
            sprint_start = datetime.strptime(sprint_start_date, "%Y-%m-%d")
        else:
            # Assuming the sprint starts on the next specified weekday from today
            today = datetime.today()
            sprint_start_weekday = get_weekday_number(sprint_set_up['sprint_begins_on'])
            sprint_start = get_next_weekday(today, sprint_start_weekday)
        
        # Determine sprint end date
        sprint_end = sprint_start + timedelta(weeks=sprint_set_up['sprint_duration']) - timedelta(days=1)
    
        # Schedule planning ceremony
        planning = team_ceremonies_settings['ceremonies']['planning']
        if planning['when'] == CeremonyStartOptions.BEGINNING.value:
            planning_start_time = planning['starts']
            planning_end_time = planning['ends']
           
            # Schedule on sprint_start date
            planning_datetime_start = datetime.combine(sprint_start, time(hour=int(planning_start_time.split(":")[0]), minute=int(planning_start_time.split(":")[1])))
            planning_datetime_end = datetime.combine(sprint_end, time(hour=int(planning_end_time.split(":")[0]), minute=int(planning_end_time.split(":")[1])))

            schedule.append({
                'type': CeremonyType.PLANNING.value,
                'starts': planning_datetime_start,
                'ends': planning_datetime_end,
                'google_meet_config': planning['google_meet_config'],
                'status': CeremonyStatus.NOT_HAPPENED_YET.value,
                # 'meeting_code': 'PlanningS32024',
                # 'date': 'Mon 05/03',
                # 'duration': '1 hr 30 mins',
                # 'team_members': team_members
            })
    