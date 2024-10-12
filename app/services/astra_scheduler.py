from datetime import timedelta, datetime, time
from bson import ObjectId
import pprint

from app.models.configurations import SprintStatus
from app.models.configurations import CeremonyStartOptions, CeremonyType, CeremonyStatus


def get_quarter(date):
    return (date.month - 1) // 3 + 1

def get_weekday_number(weekday_str):
    '''
    Convert weekday string to its corresponding integer
    '''
    weekdays = {
        'mon': 0,
        'tue': 1,
        'wed': 2,
        'thu': 3,
        'fri': 4,
    }
    return weekdays[weekday_str.lower()]

def get_next_weekday(start_date, weekday):
    '''
    Get the next date for the given weekday starting from start_date
    '''
    days_ahead = weekday - start_date.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def is_same_quarter(date1, date2):
    return get_quarter(date1) == get_quarter(date2) and date1.year == date2.year

def generate_sprints_for_quarter(selected_date, sprint_duration, team_id, latest_sprint_number):
    '''
    Generate sprints for the entire quarter based on the selected start date.
    '''
    # Determine the quarter and year from the selected date
    selected_quarter = get_quarter(selected_date)
    year = selected_date.year

    # Generate sprints
    sprints = []
    sprint_number = 1
    sprint_start_date = selected_date

    # Continue generating sprints until the sprint start date is outside the quarter
    while is_same_quarter(sprint_start_date, selected_date):
        # Calculate sprint end date based on the sprint duration
        sprint_end_date = sprint_start_date + timedelta(weeks=sprint_duration) - timedelta(days=1)

        # Create sprint document
        sprint = {
            'name': f"S{latest_sprint_number + sprint_number}-Q{selected_quarter}-{year}",
            'sprint_number': sprint_number,
            'quarter': selected_quarter,
            'year': year,
            'start_date': sprint_start_date,
            'end_date': sprint_end_date,
            'status': SprintStatus.FUTURE.value,
            'team': ObjectId(team_id),
        }

        sprints.append(sprint)

        # Prepare for next sprint
        sprint_start_date = sprint_end_date + timedelta(days=1)
        sprint_number += 1

        # Break the loop if the sprint start date is outside the quarter boundaries
        if get_quarter(sprint_start_date) != selected_quarter:
            break

    return sprints

def generate_ceremonies_for_sprint(team_ceremonies_settings, curr_sprint):
    schedule = []

    # Schedule planning ceremony
    planning = generate_planning_ceremony(team_ceremonies_settings['planning'], curr_sprint)
    schedule.append(planning)

    # Schedule standup ceremonies
    # standups = generate_standup_ceremonies(team_ceremonies_settings['standup'], curr_sprint)
    # schedule.extend(standups)

    # # Schedule retrospective ceremony
    retro = generate_retrospective_ceremony(team_ceremonies_settings['retrospective'], curr_sprint)
    schedule.append(retro)

    for ceremony in schedule: pprint.pprint(ceremony)

    return schedule
      
def generate_planning_ceremony(team_planning_settings, curr_sprint):
    planning_start_time = team_planning_settings['starts']
    planning_end_time = team_planning_settings['ends']

    sprint_start_date_time = curr_sprint['start_date']['$date']
    sprint_end_date_time = curr_sprint['start_date']['$date']

    if team_planning_settings['when'] == CeremonyStartOptions.BEGINNING.value:
        # Schedule on sprint_start date
        planning_date = datetime.date(datetime.strptime(sprint_start_date_time, '%Y-%m-%dT%H:%M:%S%z'))
    else:
        # Schedule on sprint_end date. This is the planning for the next sprint
        planning_date = datetime.date(datetime.strptime(sprint_end_date_time, '%Y-%m-%dT%H:%M:%S%z'))

    planning_datetime_start = datetime.combine(planning_date, time(hour=int(planning_start_time.split(":")[0]), minute=int(planning_start_time.split(":")[1])))
    planning_datetime_end = datetime.combine(planning_date, time(hour=int(planning_end_time.split(":")[0]), minute=int(planning_end_time.split(":")[1])))
    
    return {
        'ceremony_type': CeremonyType.PLANNING.value,
        'starts': planning_datetime_start,
        'ends': planning_datetime_end,
        'google_meet_config': team_planning_settings['google_meet_config'],
        'ceremony_status': CeremonyStatus.NOT_HAPPENED_YET.value,
        'happens_on_sprint': {
            '_id': ObjectId(curr_sprint['_id']['$oid']),
            'name': curr_sprint['name']
        },
        'team': ObjectId(curr_sprint['team']['$oid']),
        # 'refers_to_sprint': 'TODO?', 
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

def generate_retrospective_ceremony(team_retro_settings, curr_sprint):
    retro_start_time = team_retro_settings['starts']
    retro_end_time = team_retro_settings['ends']

    sprint_start_date_time = curr_sprint['start_date']['$date']
    sprint_end_date_time = curr_sprint['start_date']['$date']

    if team_retro_settings['when'] == CeremonyStartOptions.BEGINNING.value:
        # Schedule on sprint_start date
        retro_date = datetime.date(datetime.strptime(sprint_start_date_time, '%Y-%m-%dT%H:%M:%S%z'))
    else:
        # Schedule on sprint_end date. This is the planning for the next sprint
        retro_date = datetime.date(datetime.strptime(sprint_end_date_time, '%Y-%m-%dT%H:%M:%S%z'))

    retro_datetime_start = datetime.combine(retro_date, time(hour=int(retro_start_time.split(":")[0]), minute=int(retro_start_time.split(":")[1])))
    retro_datetime_end = datetime.combine(retro_date, time(hour=int(retro_end_time.split(":")[0]), minute=int(retro_end_time.split(":")[1])))
    
    return {
        'ceremony_type': CeremonyType.RETRO.value,
        'starts': retro_datetime_start,
        'ends': retro_datetime_end,
        'google_meet_config': team_retro_settings['google_meet_config'],
        'ceremony_status': CeremonyStatus.NOT_HAPPENED_YET.value,
        'happens_on_sprint': ObjectId(curr_sprint['_id']['$oid']),
        'team': ObjectId(curr_sprint['team']['$oid']),
        # 'refers_to_sprint': 'TODO?', 
        # 'meeting_code': 'PlanningS32024',
        # 'date': 'Mon 05/03',
        # 'duration': '1 hr 30 mins',
        # 'team_members': team_members
    }