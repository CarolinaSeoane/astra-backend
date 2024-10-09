from datetime import datetime, timedelta, time

from app.models.team import Team
from app.models.configurations import CeremonyStartOptions, CeremonyType, CeremonyStatus
from app.services.astra_scheduler import get_weekday_number, get_next_weekday


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
    planning = generate_planning_ceremony(team_ceremonies_settings['planning'], sprint_start, sprint_end)
    schedule.append(planning)

    # Schedule standup ceremonies
    standups = generate_standup_ceremonies(team_ceremonies_settings['standup'], sprint_start, sprint_end)
    schedule.extend(standups)

    # Schedule retrospective ceremony
    retro = generate_retrospective_ceremony(team_ceremonies_settings['retrospective'], sprint_start, sprint_end)
    schedule.append(retro)
      
def generate_planning_ceremony(team_planning_settings, sprint_start_date, sprint_end_date):
    planning_start_time = team_planning_settings['starts']
    planning_end_time = team_planning_settings['ends']

    if team_planning_settings['when'] == CeremonyStartOptions.BEGINNING.value:
        # Schedule on sprint_start date
        start_date = sprint_start_date
    else:
        # Schedule on sprint_end date
        start_date = sprint_end_date # This is the planning for the next sprint

    planning_datetime_start = datetime.combine(start_date, time(hour=int(planning_start_time.split(":")[0]), minute=int(planning_start_time.split(":")[1])))
    planning_datetime_end = datetime.combine(start_date, time(hour=int(planning_end_time.split(":")[0]), minute=int(planning_end_time.split(":")[1])))
    
    return {
        'type': CeremonyType.PLANNING.value,
        'starts': planning_datetime_start,
        'ends': planning_datetime_end,
        'google_meet_config': team_planning_settings['google_meet_config'],
        'status': CeremonyStatus.NOT_HAPPENED_YET.value,
        # 'meeting_code': 'PlanningS32024',
        # 'date': 'Mon 05/03',
        # 'duration': '1 hr 30 mins',
        # 'team_members': team_members
    }

def generate_standup_ceremonies(team_standup_settings, sprint_start_date, sprint_end_date):
    standup_days = team_standup_settings['days']
    standup_start_time = team_standup_settings['starts']
    standup_end_time = team_standup_settings['ends']
    standup_weekdays = [get_weekday_number(day) for day in standup_days]

    schedule = []
    current_date = sprint_start_date
    while current_date <= sprint_end_date:
        if current_date.weekday() in standup_weekdays:
            standup_datetime_start = current_date.replace(
                hour=int(standup_start_time.split(":")[0]),
                minute=int(standup_start_time.split(":")[1]),
                second=0,
                microsecond=0
            )
            standup_datetime_end = current_date.replace(
                hour=int(standup_end_time.split(":")[0]),
                minute=int(standup_end_time.split(":")[1]),
                second=0,
                microsecond=0
            )
            schedule.append({
                'type': CeremonyType.STANDUP.value,
                "start": standup_datetime_start,
                "end": standup_datetime_end,
                # "details": standup.get("google_meet_config", {})
            })
        current_date += timedelta(days=1)
    return schedule

def generate_retrospective_ceremony(team_retro_settings, sprint_start_date, sprint_end_date):
    pass
