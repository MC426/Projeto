from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('hospital_or_clinic_name', 'medic_name', 'start_time', 'end_time', 'current_capacity', 'max_capacity')
    list_filter = ('hospital_or_clinic_name', 'medic_name')
    search_fields = ('hospital_or_clinic_name', 'medic_name', 'location')
    list_editable = ('current_capacity', 'max_capacity')

# Register your models here.

admin.site.register(Appointment, AppointmentAdmin)
