from django.db import models
from user_api.models import AppUser

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    start_ts = models.DateTimeField()
    end_ts = models.DateTimeField()
    paciente = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='paciente_appointments',null=True, default=None )
    medico = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='medico_appointments', default=None)
    REQUIRED_FIELDS = ['start_ts', 'end_ts', 'medico']

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['name']

class RoomReservation(models.Model):
    id = models.AutoField(primary_key=True)
    start_ts = models.DateTimeField()
    end_ts = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_reserved', default=None)
    medico = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='medico_room_reservations', default=None)
    REQUIRED_FIELDS = ['start_ts', 'end_ts', 'medico']