from datetime import datetime, timedelta, timezone
from rest_framework.exceptions import ValidationError


class AppointmentValidator: 
    def validate(self, start_ts, end_ts, clock = None):
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
        if start_ts.date() != end_ts.date():
            raise ValidationError('start_ts and end_ts must be in the same day.')
        if end_ts - start_ts > timedelta(hours = 5):
            raise ValidationError('Appointment must last less than 5 hours.')
        return True
    
class PasswordValidator:
    def validate(self, password):
        if (not any(char.isupper() for char in password)):
            raise ValidationError('Password must have an uppercase character')
        
        if (len(password) < 8):
            raise ValidationError('Password must have at least 8 characters')
        
        if (not any(char.isdigit() for char in password)):
            raise ValidationError('Password must have a number')
        
        return True