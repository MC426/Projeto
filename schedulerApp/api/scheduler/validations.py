from datetime import datetime, timedelta, timezone
from rest_framework.exceptions import ValidationError

class ScheduleValidator:

    def validate_interval_consistency(self, start_ts, end_ts, clock = None):
        if clock is None:
            clock = datetime.now(timezone.utc)
        if not start_ts or not end_ts:
            raise ValidationError('Both start_ts and end_ts must be provided.')
        start_ts = start_ts.astimezone(timezone.utc)
        end_ts = end_ts.astimezone(timezone.utc)
        if start_ts > end_ts:
            raise ValidationError('start_ts must be less than end_ts.')
        if start_ts < clock:
            raise ValidationError('start_ts must be greater than now.')
        if end_ts < clock:
            raise ValidationError('end_ts must be greater than now.')

    def validate_appointment(self, start_ts, end_ts, clock = None):
        self.validate_interval_consistency(start_ts, end_ts, clock = None)
        if end_ts - start_ts > timedelta(hours = 5):
            raise ValidationError('Appointment must last less than 5 hours.')
        return True
    
    def validate_room_reservation(self, start_ts, end_ts, clock = None):
        self.validate_interval_consistency(start_ts, end_ts, clock = None)
        if end_ts - start_ts > timedelta(hours = 24):
            raise ValidationError('Room reservation must last less than 24 hours.')
        return True