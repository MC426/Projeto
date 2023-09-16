from django.shortcuts import render
from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer


# Create your views here

class AppointmentView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()