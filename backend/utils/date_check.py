from datetime import datetime

def commercial_time_check(date: datetime) -> bool:

    """"Checks whether a date is valid for a medical appointment. A date will be considered valid if it is not in the past
    or outside commercial time (Mon-Fri 8am-18h)

    Args:
        - Datetime object representing the appointment date

    Returns:
        - Bool representing whether the provided date is valid"""
    
    #Checks for past date:
    if datetime.now() > date:
        return False
    
    #Checks for invalid weekend appointment:
    if date.weekday() >= 5:
        return False
    
    #Checks for out of commercial time appointment:
    if date.hour > 18 or date.hour < 8:
        return False

    return True