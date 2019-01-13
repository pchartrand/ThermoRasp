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