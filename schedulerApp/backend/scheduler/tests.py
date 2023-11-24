from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from .models import Appointment
from .serializers import AppointmentSerializer
from user_api.models import AppUser

class AppointmentTests(TestCase):
    def setUp(self):
        AppUser.objects.create(email='user1@a.com', password='teste')
        AppUser.objects.create(email='user2@a.com', password='teste')
        AppUser.objects.create(email='medico1@a.com', password='teste')
        AppUser.objects.create(email='teste@a.com', password='teste')
        self.client = APIClient()
        self.clock_time = datetime(2023,1,1)
    
    def test_appointment_operations(self):
        user1 = AppUser.objects.get(email = 'user1@a.com')
        user2 = AppUser.objects.get(email = 'user2@a.com')
        medico = AppUser.objects.get(email = 'medico1@a.com')
        url_create = reverse('create')
        data_schedule = { 
            'start_ts' : self.clock_time,
            'end_ts' : self.clock_time + timedelta(hours = 1), 
            'medico' : medico.user_id,
            'paciente' : user1.user_id,
        }
        response_create = self.client.post(url_create, data_schedule, format = 'json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        # List appointments for the created user
        url_list = reverse('list')
        response_list = self.client.get(url_list, {'medico_id': medico.user_id})
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.data), 1)  # Assuming only one appointment is created
        # List appointments with incomplete query parameters
        url_list_incomplete = reverse('list') + '?medico_id='
        response_list_incomplete = self.client.get(url_list_incomplete)
        self.assertEqual(response_list_incomplete.status_code, status.HTTP_400_BAD_REQUEST)
        # Custom validation with invalid date format
        url_validation_invalid_date = reverse('create')
        data_validation_invalid_date = {
            'start_ts': 'invalid_date',
            'end_ts': 'invalid_date',
            'medico': medico.user_id,
            'paciente': user1.user_id,
        }
        response_validation_invalid_date = self.client.post(url_validation_invalid_date, data_validation_invalid_date, format='json')
        self.assertEqual(response_validation_invalid_date.status_code, status.HTTP_400_BAD_REQUEST)

        # Custom validation with missing fields
        url_validation_missing_fields = reverse('create')
        data_validation_missing_fields = {
            'medico': medico.user_id,
            'paciente': user1.user_id,
        }
        response_validation_missing_fields = self.client.post(url_validation_missing_fields, data_validation_missing_fields, format='json')
        self.assertEqual(response_validation_missing_fields.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_ts', response_validation_missing_fields.data)
        self.assertIn('end_ts', response_validation_missing_fields.data)
        # Create another appointment
        url_create_another = reverse('create')
        data_create_another = {
            'start_ts': self.clock_time + timedelta(hours = 2),
            'end_ts': self.clock_time + timedelta(hours=3),
            'medico': medico.user_id,
            'paciente': user2.user_id,
        }
        response_create_another = self.client.post(url_create_another, data_create_another, format='json')
        self.assertEqual(response_create_another.status_code, status.HTTP_201_CREATED)
        # List appointments with invalid query parameters
        url_list_invalid_params = reverse('list') + '?invalid_param=1'
        response_list_invalid_params = self.client.get(url_list_invalid_params)
        self.assertEqual(response_list_invalid_params.status_code, status.HTTP_400_BAD_REQUEST)

        # List appointments with negative query parameters
        url_list_negative_params = reverse('list') + '?medico_id=-1'
        response_list_negative_params = self.client.get(url_list_negative_params)
        self.assertEqual(response_list_negative_params.status_code, status.HTTP_200_OK)
        # Create a third appointment with overlap
        url_create_third = reverse('create')
        data_create_third = {
            'start_ts': self.clock_time,
            'end_ts': self.clock_time + timedelta(hours=2),
            'medico': medico.user_id,
            'paciente': user2.user_id,
        }

        # Print data for debugging
        # print('Creating a third appointment with overlap. Data:', data_create_third)

        response_create_third = self.client.post(url_create_third, data_create_third, format='json')
        self.assertEqual(response_create_third.status_code, status.HTTP_400_BAD_REQUEST)
        # print('Response for creating a third appointment with overlap:', response_create_third.data)

        #if response_create_third.status_code == status.HTTP_400_BAD_REQUEST:
        #    print('Validation error:', response_create_third.data)
        # Create a appointment with overlap of end, but not start:
        data_create_4 = {
            'start_ts': self.clock_time + timedelta(hours=-1),
            'end_ts': self.clock_time + timedelta(hours=0.5),
            'medico': medico.user_id,
            'paciente': user2.user_id,
        }
        response_create_4 = self.client.post(url_create, data_create_4, format='json')
        self.assertEqual(response_create_4.status_code, status.HTTP_400_BAD_REQUEST)
