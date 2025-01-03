from datetime import datetime


def get_current_time() -> tuple:
    now = datetime.now()
    current_time = now.hour * 60 + now.minute
    current_day = now.day
    current_month = now.month
    current_year = now.year

    # Perhaps may need
    # current_time_in_sec = now.hour * 3600 + now.minute * 60 + now.second
    # current_second = now.second

    return current_time, current_day, current_month, current_year
