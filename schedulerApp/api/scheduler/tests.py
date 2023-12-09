from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from .models import Appointment, Room, RoomReservation
from user_api.models import AppUser
from .models import Appointment, Room, RoomReservation
from user_api.models import AppUser
from .serializers import AppointmentSerializer
from user_api.models import AppUser
from .validations import ScheduleValidator, PasswordValidator
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta, timezone


class AppointmentTests(TestCase):
    def setUp(self):
        AppUser.objects.create(email='user1@a.com', password='teste')
        AppUser.objects.create(email='user2@a.com', password='teste')
        AppUser.objects.create(email='medico1@a.com', password='teste')
        AppUser.objects.create(email='teste@a.com', password='teste')
        self.client = APIClient()
        self.clock_time = datetime(2200, 1, 1)
        self.url_create = reverse('create-appointment')
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
        url_validation_invalid_date = reverse('create-appointment')
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
        url_validation_missing_fields = reverse('create-appointment')
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlap_same_time(self):
        self.create_appointment_test(self.clock_time, self.clock_time + timedelta(hours = 1))
        response = self.create_appointment_test(self.clock_time, self.clock_time + timedelta(hours=1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AppointmentValidatorTest(TestCase):
    def setUp(self):
        self.clock_time = datetime(2023,1,1,0,0,0,0,timezone.utc) # 2023-01-01 00:00:00 UTC
        self.validator = ScheduleValidator()
        self.validator = ScheduleValidator()
    '''
        Testes de acordo com classe de equivalência:
        As classes invalidas sao:
        1. start_ts > end_ts
        2. start_ts < clock
        3. end_ts < clock
        4. end_ts - start_ts > 5 hours
        4. end_ts - start_ts > 5 hours
        As classes validas sao:
        1. start_ts < end_ts and start_ts > clock and end_ts > clock and start_ts.date() == end_ts.date() and end_ts - start_ts > 5 hours
    '''
    # 1. start_ts > end_ts 
    def test_termina_depois_comeco(self):
        with self.assertRaises(ValidationError):
            self.validator.validate_appointment(self.clock_time + timedelta(hours=1), self.clock_time, self.clock_time)
    
    # 2. start_ts < clock
    def test_comeca_passado(self):
        with self.assertRaises(ValidationError):
            self.validator.validate_appointment(self.clock_time - timedelta(hours=1), self.clock_time + timedelta(hours=1), self.clock_time) 
    
    # 3. end_ts < clock
    def test_termina_passado(self):
        with self.assertRaises(ValidationError):
            self.validator.validate_appointment(self.clock_time + timedelta(hours=1), self.clock_time + timedelta(hours=-2), self.clock_time)

    # 4. end_ts - start_ts > 5 hours
    def test_dura_muito_tempo(self):
        with self.assertRaises(ValidationError):
            self.validator.validate_appointment(self.clock_time + timedelta(hours=1), self.clock_time + timedelta(hours=7), self.clock_time)
    
    # 5. start_ts < end_ts and start_ts > clock and end_ts > clock and start_ts.date() == end_ts.date() and end_ts - start_ts <= 5 hours
    def test_classe_valida(self):
        self.validator.validate_appointment(self.clock_time + timedelta(hours=5), self.clock_time + timedelta(hours=5), self.clock_time)
    
class RoomTests(TestCase):
    
    def setUp(self):
        self.room = Room.objects.create(name='Sala Teste')
        self.client = APIClient()
        self.url = reverse('manage-rooms')
        
    def test_create_room(self):

        data = {
            'name': 'Sala Teste 2'
        }

        try:
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            created_room = Room.objects.get(name='Sala Teste 2')
            self.assertEqual(created_room.name, 'Sala Teste 2')
        finally:
            created_room = Room.objects.filter(name='Sala Teste 2')
            if created_room:
                created_room.delete()

    def test_update_room(self):

        data = {
            'id': self.room.id,
            'name': 'Sala Teste atualizada'
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Room.objects.get(id=self.room.id).name, 'Sala Teste atualizada')
    
    def test_list_rooms(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_room(self):

        data = {
            'id': self.room.id,
        }
        response = self.client.delete(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        deleted_room = Room.objects.filter(id=self.room.id)
        self.assertFalse(deleted_room)

    def tearDown(self):
        if Room.objects.filter(id=self.room.id):
            self.room.delete()

class RoomReservationTests(TestCase):

    '''Realizaremos testes de acordo com análise de valor limite.
    Como a função de validação de grande parte de start_ts e end_ts é a mesma
    usada para o agendamento de consultas, que já possui testes escritos considerando as classes
    de equivalência, testaremos apenas as particularidades do código de agendamento de salas.

    Os valores limite são:

    1. end_ts - start_ts = 24 horas (válida)
    2. end_ts - start_ts = 24 horas + 1 minuto (inválida)
    3. start_ts_outra_consulta = end_ts (válida)
    4. start_ts_outra_consulta = end_ts - 1 minuto (inválida)
    5. start_ts = end_outra_consulta (válida)
    6. start_ts = end_outra_consulta - 1 minuto (inválida)

    '''

    def setUp(self):
        self.room = Room.objects.create(name='Sala Teste')
        self.medico = AppUser.objects.create(email='teste@teste.com', username='medico', is_staff=False)
        self.client = APIClient()
        self.reservation = RoomReservation.objects.create(
            room=self.room,
            start_ts=datetime(2028,1,2,0,0,0,0,timezone.utc),
            end_ts=datetime(2028,1,2,5,0,0,0,timezone.utc),
            medico=self.medico
        )
        self.reservation.save()
        self.url = reverse('manage-room-reservations')
    
    def test_limit_1(self):
            
        data = {
            'room': self.room.id,
            'start_ts': datetime(2028,1,5,0,0,0,0,timezone.utc),
            'end_ts': datetime(2028,1,6,0,0,0,0,timezone.utc),
            'medico': self.medico.user_id
        }
    
        try:
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        finally:
            created_reservation = RoomReservation.objects.filter(start_ts=datetime(2028,1,5,0,0,0,0,timezone.utc))
            if created_reservation:
                created_reservation.delete()
    
    def test_limit_2(self):
                
        data = {
            'room': self.room.id,
            'start_ts': datetime(2028,1,10,0,0,0,0,timezone.utc),
            'end_ts': datetime(2028,1,11,0,1,0,0,timezone.utc),
            'medico': self.medico.user_id
        }
        
        try:
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        finally:
            created_reservation = RoomReservation.objects.filter(start_ts=datetime(2028,1,10,0,0,0,0,timezone.utc))
            if created_reservation:
                created_reservation.delete()

    def test_limit_3(self):

        #Termina quando a self.reservation começa
        data = {
            'room': self.room.id,
            'start_ts': datetime(2028,1,1,22,0,0,0,timezone.utc),
            'end_ts': datetime(2028,1,2,0,0,0,0,timezone.utc),
            'medico': self.medico.user_id
        }

        try:
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        finally:
            created_reservation = RoomReservation.objects.filter(start_ts=datetime(2028,1,1,22,0,0,0,timezone.utc))
            if created_reservation:
                created_reservation.delete()

    def test_limit_4(self):

        #Termina 1 minuto depois da self.reservation começar
        data = {
            'room': self.room.id,
            'start_ts': datetime(2028,1,1,22,0,0,0,timezone.utc),
            'end_ts': datetime(2028,1,2,0,1,0,0,timezone.utc),
            'medico': self.medico.user_id
        }

        try:
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        finally:
            created_reservation = RoomReservation.objects.filter(start_ts=datetime(2028,1,1,22,0,0,0,timezone.utc))
            if created_reservation:
                created_reservation.delete()

    def test_limit_5(self):

        #Começa quando a self.reservation termina
        data = {
            'room': self.room.id,
            'start_ts': datetime(2028,1,2,5,0,0,0,timezone.utc),
            'end_ts': datetime(2028,1,2,6,0,0,0,timezone.utc),
            'medico': self.medico.user_id
        }

        try:
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        finally:
            created_reservation = RoomReservation.objects.filter(start_ts=datetime(2028,1,1,5,0,0,0,timezone.utc))
            if created_reservation:
                created_reservation.delete()

    def test_limit_6(self):

        #Começa 1 minuto antes da self.reservation terminar
        data = {
            'room': self.room.id,
            'start_ts': datetime(2028,1,2,4,59,0,0,timezone.utc),
            'end_ts': datetime(2028,1,2,6,0,0,0,timezone.utc),
            'medico': self.medico.user_id
        }

        try:
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        finally:
            created_reservation = RoomReservation.objects.filter(start_ts=datetime(2028,1,1,4,59,0,0,timezone.utc))
            if created_reservation:
                created_reservation.delete()

    def tearDown(self):
        self.reservation.delete()
        self.medico.delete()
        self.room.delete()

class PasswordTest(TestCase):
    def setUp(self):
        self.validator = PasswordValidator()
    '''
        Testes de acordo com classe de equivalência:
        As classes invalidas sao:
        1. nao tem letra maiuscula
        2. < 8 caracteres
        3. nao tem numero
        As classes validas sao:
        1. Tem letra maiuscula and >= 8 caracteres and tem numero
    '''
    # 1. nao tem letra maiuscula
    def test_no_upper(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('naimshaikhzadeh12')
    
    # 2. < 8 caracteres
    def test_small(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('Bruno00') 
    
    # 3. nao tem numero
    def test_no_number(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('LuizHenriqueYujiDelgadoOda')
    
    # 4. Tem letra maiuscula and >= 8 caracteres and tem numero
    def test_valid(self):
        self.validator.validate('AndreasCisiRamos2003')
    
