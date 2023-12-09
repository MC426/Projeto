from django.contrib import admin
from .models import Appointment, Room, RoomReservation

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('start_ts', 'end_ts', 'paciente', 'medico')
    list_filter = ('medico', 'paciente')
    search_fields = ('medico', 'paciente')

# Register your models here.

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(RoomReservation)
admin.site.register(Room)