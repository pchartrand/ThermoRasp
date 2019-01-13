import datetime
TZ = 5


class Week(object):
    def __init__(self):
        self.week_start = self._weekstart(datetime.datetime.now()+ datetime.timedelta(hours=-TZ))

    @staticmethod
    def _weekstart(current_time):
        return current_time - datetime.timedelta(
            hours=current_time.hour,
            minutes=current_time.minute,
            days=current_time.weekday()
        )

    def event_time_in_week(self, day, event):
        return self.week_start + datetime.timedelta(days=day, hours=event.hour, minutes=event.minute)

    def minute_prior_to_event(self, day, event):
        return self.event_time_in_week(day, event) - datetime.timedelta(minutes=1)
