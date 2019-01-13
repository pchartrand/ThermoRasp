import datetime

DATETIME_SECONDS = '%Y-%m-%d %H:%M:%S'
DATETIME_MINUTES = '%Y-%m-%d %H:%M'
TZ = 5


def now():
    return datetime.datetime.now()+ datetime.timedelta(hours=-TZ)


def time_to_seconds(time=now()):
    return time.strftime(DATETIME_SECONDS)


def time_to_minutes(time=now()):
    return time.strftime(DATETIME_MINUTES)


def weekstart(current_time):
    return current_time - datetime.timedelta(hours=current_time.hour, minutes=current_time.minute,days=current_time.weekday())


def event_time_in_week(week_start, day, event):
    return week_start + datetime.timedelta(days=day, hours=event.hour, minutes=event.minute)

def minute_prior_to_event(week_start, day, event):
    return event_time_in_week(week_start, day, event) - datetime.timedelta(minutes=1)
