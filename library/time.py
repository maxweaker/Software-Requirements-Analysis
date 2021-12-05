from datetime import timedelta, datetime
from django.utils import timezone

def datecompare(dateA, dateB, days, minutes, hours, weeks):
    time = timedelta(days=days, minutes=minutes, hours=hours, weeks=weeks)

    if dateB.__ge__(dateA + time):
        return True
    else:
        return False


def dateadd(date, days, minutes, hours, weeks):
    time = date + timedelta(days=days, minutes=minutes, hours=hours, weeks=weeks)
    return time


def datedel(date, days, minutes, hours, weeks):
    time = date - timedelta(days=days, minutes=minutes, hours=hours, weeks=weeks)
    return time



