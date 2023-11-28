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
        self.clock_time = datetime(2023, 1, 1)
        self.url_create = reverse('create')
        self.url_list = reverse('list')
        
    def create_appointment(self, start_ts, end_ts, medico, paciente):
        data_schedule = {
            'start_ts': start_ts,
            'end_ts': end_ts,
            'medico': medico.user_id,
            'paciente': paciente.user_id,
        }
        return self.client.post(self.url_create, data_schedule, format='json')


    def test_create_appointment(self):
        user1 = AppUser.objects.get(email='user1@a.com')
        medico = AppUser.objects.get(email='medico1@a.com')
        response_create = self.create_appointment(self.clock_time, self.clock_time + timedelta(hours=1), medico, user1)
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

    def test_list_appointments_for_medico(self):
        user1 = AppUser.objects.get(email='user1@a.com')
        medico = AppUser.objects.get(email='medico1@a.com')
        self.create_appointment(self.clock_time, self.clock_time + timedelta(hours=1), medico, user1)
        response_list = self.client.get(self.url_list, {'medico_id': medico.user_id})
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.data), 1)
    
    def test_list_appointments_for_paciente(self):
        user1 = AppUser.objects.get(email='user1@a.com')
        medico = AppUser.objects.get(email='medico1@a.com')
        self.create_appointment(self.clock_time, self.clock_time + timedelta(hours=1), medico, user1)
        response_list = self.client.get(self.url_list, {'paciente_id': user1.user_id})
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.data), 1)

    def test_list_appointments_with_incomplete_parameters(self):
        url_list_incomplete = reverse('list') + '?medico_id='
        response_list_incomplete = self.client.get(url_list_incomplete)
        self.assertEqual(response_list_incomplete.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validation_with_invalid_date_format(self):
        medico = AppUser.objects.get(email='medico1@a.com')
        user1 = AppUser.objects.get(email='user1@a.com')
        url_validation_invalid_date = reverse('create')
        data_validation_invalid_date = {
            'start_ts': 'invalid_date',
            'end_ts': 'invalid_date',
            'medico': medico.user_id,
            'paciente': user1.user_id,
        }
        response_validation_invalid_date = self.client.post(url_validation_invalid_date, data_validation_invalid_date,
                                                            format='json')
        self.assertEqual(response_validation_invalid_date.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validation_with_missing_fields(self):
        medico = AppUser.objects.get(email='medico1@a.com')
        user1 = AppUser.objects.get(email='user1@a.com')
        url_validation_missing_fields = reverse('create')
        data_validation_missing_fields = {
            'medico': medico.user_id,
            'paciente': user1.user_id,
        }
        response_validation_missing_fields = self.client.post(url_validation_missing_fields,
                                                              data_validation_missing_fields, format='json')
        self.assertEqual(response_validation_missing_fields.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_ts', response_validation_missing_fields.data)
        self.assertIn('end_ts', response_validation_missing_fields.data)

    def test_list_appointments_with_invalid_parameters(self):
        url_list_invalid_params = reverse('list') + '?invalid_param=1'
        response_list_invalid_params = self.client.get(url_list_invalid_params)
        self.assertEqual(response_list_invalid_params.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_appointments_with_negative_parameters(self):
        url_list_negative_params = reverse('list') + '?medico_id=-1'
        response_list_negative_params = self.client.get(url_list_negative_params)
        self.assertEqual(response_list_negative_params.status_code, status.HTTP_200_OK)


    def create_appointment_test(self, start_ts, end_ts):
        user2 = AppUser.objects.get(email='user2@a.com')
        medico = AppUser.objects.get(email='medico1@a.com')
        return self.create_appointment(start_ts, end_ts, medico, user2)


    def test_overlap_start_middle(self):
        self.create_appointment_test(self.clock_time, self.clock_time + timedelta(hours = 1))
        response = self.create_appointment_test(self.clock_time + timedelta(minutes=30), self.clock_time + timedelta(hours=1, minutes=30))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlap_start_past(self):
        self.create_appointment_test(self.clock_time, self.clock_time + timedelta(hours = 1))
        response = self.create_appointment_test(self.clock_time - timedelta(hours=1), self.clock_time + timedelta(minutes=30))                 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

    def test_overlap_middle(self):
        self.create_appointment_test(self.clock_time, self.clock_time + timedelta(hours = 1))
        response = self.create_appointment_test(self.clock_time + timedelta(minutes=30), self.clock_time + timedelta(minutes=45))
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlap_same_time(self):
        self.create_appointment_test(self.clock_time, self.clock_time + timedelta(hours = 1))
        response = self.create_appointment_test(self.clock_time, self.clock_time + timedelta(hours=1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
