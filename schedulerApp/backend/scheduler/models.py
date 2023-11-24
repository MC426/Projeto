from django.db import models
from user_api.models import AppUser

# Create your models here.
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    start_ts = models.DateTimeField()
    end_ts = models.DateTimeField()
    paciente = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='paciente_appointments',null=True, default=None )
    medico = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='medico_appointments', default=None)
    REQUIRED_FIELDS = ['start_ts', 'end_ts', 'medico']