# serializers.py
from rest_framework import serializers
from .models import Appointment, RoomReservation, Room

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'start_ts', 'end_ts', 'paciente', 'medico']

class RoomReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = ['id', 'start_ts', 'end_ts', 'medico']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_reservations']