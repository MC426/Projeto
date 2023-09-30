from django.db import models

# Create your models here.
class Appointment(models.Model):
    # Fields for the medical appointment
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()
    current_capacity = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255)
    hospital_or_clinic_name = models.CharField(max_length=255)
    medic_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Appointment at {self.hospital_or_clinic_name} with {self.medic_name} on {self.start_time}"
