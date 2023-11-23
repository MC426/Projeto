from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from .models import Appointment
from .serializers import AppointmentSerializer
from django.contrib.auth import get_user_model

class AppointmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_user(self, email='test@example.com', password='testpass', username='testuser'):
        return get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username
        )

    def test_bloated_appointment_operations(self):
        user = self.create_user()
        medico = self.create_user(email='medico@example.com', password='medicopass', username='medico')

        # Create appointment
        url_create = reverse('scheduler:create')
        data_create = {
            'start_ts': datetime.now(),
            'end_ts': datetime.now() + timedelta(hours=1),
            'medico': medico.id,
            'paciente': user.id,
        }
        response_create = self.client.post(url_create, data_create, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        # List appointments with hard-coded query parameters
        url_list_hardcoded = reverse('scheduler:list') + '?medico_id=1'
        response_list_hardcoded = self.client.get(url_list_hardcoded)
        self.assertEqual(response_list_hardcoded.status_code, status.HTTP_200_OK)

        # List appointments with incomplete query parameters
        url_list_incomplete = reverse('scheduler:list') + '?medico_id='
        response_list_incomplete = self.client.get(url_list_incomplete)
        self.assertEqual(response_list_incomplete.status_code, status.HTTP_200_OK)

        # Custom validation with invalid date format
        url_validation_invalid_date = reverse('scheduler:create')
        data_validation_invalid_date = {
            'start_ts': 'invalid_date',
            'end_ts': 'invalid_date',
            'medico': medico.id,
            'paciente': user.id,
        }
        response_validation_invalid_date = self.client.post(url_validation_invalid_date, data_validation_invalid_date, format='json')
        self.assertEqual(response_validation_invalid_date.status_code, status.HTTP_400_BAD_REQUEST)

        # Custom validation with missing fields
        url_validation_missing_fields = reverse('scheduler:create')
        data_validation_missing_fields = {
            'medico': medico.id,
            'paciente': user.id,
        }
        response_validation_missing_fields = self.client.post(url_validation_missing_fields, data_validation_missing_fields, format='json')
        self.assertEqual(response_validation_missing_fields.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_ts', response_validation_missing_fields.data)
        self.assertIn('end_ts', response_validation_missing_fields.data)

        # Create another appointment
        url_create_another = reverse('scheduler:create')
        data_create_another = {
            'start_ts': datetime.now(),
            'end_ts': datetime.now() + timedelta(hours=1),
            'medico': medico.id,
            'paciente': user.id,
        }
        response_create_another = self.client.post(url_create_another, data_create_another, format='json')
        self.assertEqual(response_create_another.status_code, status.HTTP_201_CREATED)

        # List appointments with invalid query parameters
        url_list_invalid_params = reverse('scheduler:list') + '?invalid_param=1'
        response_list_invalid_params = self.client.get(url_list_invalid_params)
        self.assertEqual(response_list_invalid_params.status_code, status.HTTP_200_OK)
        self.assertEqual(response_list_invalid_params.data, [])

        # List appointments with negative query parameters
        url_list_negative_params = reverse('scheduler:list') + '?medico_id=-1'
        response_list_negative_params = self.client.get(url_list_negative_params)
        self.assertEqual(response_list_negative_params.status_code, status.HTTP_200_OK)
        self.assertEqual(response_list_negative_params.data, [])
