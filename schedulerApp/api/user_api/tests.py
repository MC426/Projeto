from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import AppUser
from django.core.exceptions import ValidationError
from .validations import EmailValidator

class UserViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_view_url = reverse('user')
        AppUser.objects.create(email = 'user1@ex.com', username = 'user1', password = 'testpass1')
        AppUser.objects.create(email = 'user2@ex.com', username = 'user2', password = 'testpass2')

    def test_successful_registration_login_logout(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass',
            'username': 'usuario'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_login = {
            'email': 'test@example.com',
            'password': 'testpass'
        }
        response_login = self.client.post(self.login_url, data_login, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        # Get the JWT token from the response
        jwt_token = response_login.data['jwt']

        # Set the token in the client's headers for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

        # Retrieve user information
        response_user_view = self.client.get(self.user_view_url)
        self.assertEqual(response_user_view.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user_view.data['email'], 'test@example.com')

        response_logout = self.client.post(self.logout_url)
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)

        # Attempt to retrieve user information after logout
        response_user_view_after_logout = self.client.get(self.user_view_url)
        self.assertEqual(response_user_view_after_logout.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_password (self):
        data = {
            'email': 'user1@ex.com',
            'password': 'wrongpass'
        }
        response_login = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_repeated_email(self):
        data = {'email': 'test2@example.com','password': 'testpass','username': 'usuario'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {'email': 'test2@example.com','password': 'testpass','username': 'usuario'}
        with self.assertRaises(ValidationError):
            self.client.post(self.register_url, data, format='json')

    def test_view_no_JWT(self):
        response = self.client.get(self.user_view_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registration_without_email(self):
        data = {'password': 'testpass', 'username': 'usuario'}
        with self.assertRaises(KeyError):
            self.client.post(self.register_url, data, format='json')

    def test_registration_without_username(self):
        data = {'email': 'email2@example.com', 'password': 'testpass'}
        with self.assertRaises(KeyError):
            self.client.post(self.register_url, data, format='json')

    def test_registration_without_password(self):
        data = {'email': 'email3@example.com', 'username': 'usuario3'}
        with self.assertRaises(KeyError):
            self.client.post(self.register_url, data, format='json')

    
class EmailTest(TestCase):
    def setUp(self):
        self.validator = EmailValidator()
    '''
        Testes de acordo com classe de equivalência:
        As classes invalidas sao:
        1. Não tem '@'
        2. Não tem '.' no domínio
        3. A string antes do '@' não pode ser vazia
        4. A string entre o '@' e o '.' não pode ser vazia
        5. A string depois do '.' não pode ser vazia

        As classes validas sao:
        1. Tem '@' and Tem '.' and string antes do '@' > 0 and string entre '@' e '.' >0 
            and string depois do '.' > 0
    '''
    # 1. Não tem '@'
    def test_no_commercial_at(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('naimgmail.com')
    
    # 2. Não tem '.' no domínio
    def test_no_dot(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('Brun@gmailcom') 
    
    # 3. A string antes do '@' não pode ser vazia
    def test_empty_string_before_commercial_at(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('@hotmail.com')
    
    # 4. A string entre o '@' e o '.' não pode ser vazia
    def test_empty_string_between_commercial_at_and_dot(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('Andreas@.com')

    # 5. A string depois do '.' não pode ser vazia
    def test_empty_string_after_dot(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('Bernardo@gmail.')
    
    # 6. Tem '@' and Tem '.' and string antes do '@' > 0 and string entre '@' e '.' >0  and string depois do '.' > 0
    def test_valid(self):
        self.validator.validate('LuizOda@unicamp.com.br')
    
        