from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class UserViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_view_url = reverse('user')

    def test_user_views(self):
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

        # try to login with incorrect password
        data_login_bad = {
            'email': 'test@example.com',
            'password': 'WRONG-PASSWORD'
        }

        response_login = self.client.post(self.login_url, data_login_bad, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_403_FORBIDDEN)
        # Try to login with invalid email
        data_login_bad = {
            'email': 'wrong-email@example.com',
            'password': 'testpass'
        }

        response_login = self.client.post(self.login_url, data_login_bad, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Attempt to retrieve user information after logout
        response_user_view_after_logout = self.client.get(self.user_view_url)
        self.assertEqual(response_user_view_after_logout.status_code, status.HTTP_403_FORBIDDEN)

        data_sem_usuario = {
            'email': 'email2@example.com',
            'password': 'testpass'
        }
        with self.assertRaises(KeyError):
            # Wrap the code that is expected to raise an error inside this block
            response = self.client.post(self.register_url, data_sem_usuario, format='json')        

        data_sem_email = {
            'username' : 'usuario2',
            'password': 'testpass'
        }
        with self.assertRaises(KeyError):
            # Wrap the code that is expected to raise an error inside this block
            response = self.client.post(self.register_url, data_sem_email, format='json')        
        data_sem_password = {
            'username' : 'usuario2',
            'email': 'email3@example.com'
        }
        with self.assertRaises(KeyError):
            # Wrap the code that is expected to raise an error inside this block
            response = self.client.post(self.register_url, data_sem_password, format='json')        
        