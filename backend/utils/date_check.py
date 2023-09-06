from datetime import datetime, date
import holidays

def commercial_time_check(date: datetime) -> bool:

    """"Checks whether a date is valid for a medical appointment. A date will be considered valid if it is not in the past,
    during brazilian holidays, more than 2 years in the future, or outside commercial time (Mon-Fri 8am-18h)

    Args:
        - Datetime object representing the appointment date

    Returns:
        - Bool representing whether the provided date is valid"""
    
    now = datetime.now()

    #Checks for past date:
    if now > date:
        return False
    
    #Checks if the date is in the current or next year:
    if date.year - now.year > 1:
        return False
    
    #Checks for invalid weekend appointment:
    if date.weekday() >= 5:
        return False
    
    #Checks for out of commercial time appointment:
    if date.hour > 18 or date.hour < 8:
        return 
    
    #Checks for holidays:
    years = [now.year, now.year + 1]
    forbidden_dates = holidays.Brazil(years=years)
    for holiday in forbidden_dates.keys():
        if date == holiday:
            return False

    return True