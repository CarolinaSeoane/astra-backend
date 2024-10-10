from datetime import timedelta


def get_current_quarter(date):
    month = date.month
    if month in [1, 2, 3]:
        return 1
    elif month in [4, 5, 6]:
        return 2
    elif month in [7, 8, 9]:
        return 3
    else:
        return 4

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