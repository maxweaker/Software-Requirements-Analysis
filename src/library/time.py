from datetime import timedelta, datetime
from django.utils import timezone


def dateCompare(dateA, dateB, days=0, minutes=0, hours=0, weeks=0):
    time = timedelta(days=days, minutes=minutes, hours=hours, weeks=weeks)

    if dateB.__ge__(dateA + time):
        return False
    else:
        return True


def dateAdd(date, days=0, minutes=0, hours=0, weeks=0):
    time = date + timedelta(days=days, minutes=minutes, hours=hours, weeks=weeks)
    return time


def dateSub(date, days=0, minutes=0, hours=0, weeks=0):
    time = date - timedelta(days=days, minutes=minutes, hours=hours, weeks=weeks)
    return time
