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

def get_previous_friday(date):
    '''
    If the date is a sunday or saturday, it returns the previous friday
    '''    
    day_of_week = date.weekday()
    
    # Calculate how many days back we need to go to get to the previous Friday
    # If it's Sunday (6), subtract 2 days to get to Friday.
    # Otherwise, subtract the number of days passed since Friday (4).
    days_to_subtract = (day_of_week - 4) % 7
    
    return date - timedelta(days=days_to_subtract)

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
            'sprint_number': latest_sprint_number + sprint_number,
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
    planning = generate_planning_or_retro_ceremony(team_ceremonies_settings['planning'], curr_sprint, CeremonyType.PLANNING.value)
    schedule.append(planning)

    # Schedule standup ceremonies
    standups = generate_standup_ceremonies(team_ceremonies_settings['standup'], curr_sprint)
    schedule.extend(standups)

    # # Schedule retrospective ceremony
    retro = generate_planning_or_retro_ceremony(team_ceremonies_settings['retrospective'], curr_sprint, CeremonyType.RETRO.value)
    schedule.append(retro)

    for ceremony in schedule: pprint.pprint(ceremony)

    return schedule
      
def generate_planning_or_retro_ceremony(team_settings, curr_sprint, ceremony_type):
    meeting_start_time = team_settings['starts']
    meeting_end_time = team_settings['ends']

    sprint_start_date_time = datetime.date(datetime.strptime(curr_sprint['start_date']['$date'], '%Y-%m-%dT%H:%M:%S%z'))
    sprint_end_date_time = datetime.date(datetime.strptime(curr_sprint['end_date']['$date'], '%Y-%m-%dT%H:%M:%S%z'))

    if sprint_end_date_time.weekday() == 6:
        sprint_end_date_time = get_previous_friday(sprint_end_date_time)

    if team_settings['when'] == CeremonyStartOptions.BEGINNING.value:
        # Schedule on sprint_start date
        meeting_date = sprint_start_date_time
    else:
        # Schedule on sprint_end date. This is the planning for the next sprint
        meeting_date = sprint_end_date_time

    meeting_datetime_start = datetime.combine(meeting_date, time(hour=int(meeting_start_time.split(":")[0]), minute=int(meeting_start_time.split(":")[1])))
    meeting_datetime_end = datetime.combine(meeting_date, time(hour=int(meeting_end_time.split(":")[0]), minute=int(meeting_end_time.split(":")[1])))
    
    return {
        'ceremony_type': ceremony_type,
        'starts': meeting_datetime_start,
        'ends': meeting_datetime_end,
        'google_meet_config': team_settings['google_meet_config'],
        'ceremony_status': CeremonyStatus.NOT_HAPPENED_YET.value,
        'happens_on_sprint': {
            '_id': ObjectId(curr_sprint['_id']['$oid']),
            'name': curr_sprint['name']
        },
        'team': ObjectId(curr_sprint['team']['$oid']),
        # 'refers_to_sprint': 'TODO?', 
        # 'duration': '1 hr 30 mins',
        # 'team_members': team_members
    }

def generate_standup_ceremonies(team_settings, curr_sprint):
    standup_days = team_settings['days']
    standup_start_time = team_settings['starts']
    standup_end_time = team_settings['ends']
    standup_weekdays = [get_weekday_number(day) for day in standup_days]

    schedule = []

    current_date = datetime.date(datetime.strptime(curr_sprint['start_date']['$date'], '%Y-%m-%dT%H:%M:%S%z'))
    sprint_end_date = datetime.date(datetime.strptime(curr_sprint['end_date']['$date'], '%Y-%m-%dT%H:%M:%S%z'))
    while current_date <= sprint_end_date:
        if current_date.weekday() in standup_weekdays:
            standup_datetime_start = datetime.combine(current_date, time(hour=int(standup_start_time.split(":")[0]), minute=int(standup_start_time.split(":")[1])))
            standup_datetime_end = datetime.combine(current_date, time(hour=int(standup_end_time.split(":")[0]), minute=int(standup_end_time.split(":")[1])))
            schedule.append({
                'ceremony_type': CeremonyType.STANDUP.value,
                "starts": standup_datetime_start,
                "ends": standup_datetime_end,
                'google_meet_config': team_settings['google_meet_config'],
                'ceremony_status': CeremonyStatus.NOT_HAPPENED_YET.value,
                'happens_on_sprint': {
                    '_id': ObjectId(curr_sprint['_id']['$oid']),
                    'name': curr_sprint['name']
                },
                'team': ObjectId(curr_sprint['team']['$oid']),
            })
        current_date += timedelta(days=1)
    return schedule
