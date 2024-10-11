from datetime import timedelta
from bson import ObjectId

from app.models.configurations import SprintStatus


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