# tests/auth.spec.py

import jwt
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings
from accounts.models import User, Organisation

class AuthTests(APITestCase):

    def test_register_user_successfully(self):
        url = reverse('register')
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'phone': '1234567890',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], 'John')
        self.assertEqual(response.data['data']['user']['email'], 'john@example.com')

        # Check the organisation
        organisation = Organisation.objects.get(name="John's Organisation")
        self.assertIsNotNone(organisation)
        self.assertIn(User.objects.get(email='john@example.com'), organisation.users.all())

    def test_register_user_validation_error(self):
        url = reverse('register')
        data = {
            'firstName': '',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'phone': '1234567890',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['status'], 'Bad request')

    def test_register_user_duplicate_email(self):
        User.objects.create_user(
            email='john@example.com',
            firstName='John',
            lastName='Doe',
            password='password123'
        )
        url = reverse('register')
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'phone': '1234567890',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['status'], 'Bad request')

    def test_login_user_successfully(self):
        user = User.objects.create_user(
            email='john@example.com',
            firstName='John',
            lastName='Doe',
            password='password123'
        )
        url = reverse('login')
        data = {
            'email': 'john@example.com',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])

    def test_login_user_invalid_credentials(self):
        user = User.objects.create_user(
            email='john@example.com',
            firstName='John',
            lastName='Doe',
            password='password123'
        )
        url = reverse('login')
        data = {
            'email': 'john@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Authentication failed')

    def test_token_generation(self):
        user = User.objects.create_user(
            email='john@example.com',
            firstName='John',
            lastName='Doe',
            password='password123'
        )
        token = user.get_jwt_token()
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(decoded['userId'], user.userId)
        self.assertIn('exp', decoded)
        self.assertTrue(datetime.fromtimestamp(decoded['exp']) > datetime.utcnow())

    def test_user_detail_access(self):
        user = User.objects.create_user(
            email='john@example.com',
            firstName='John',
            lastName='Doe',
            password='password123'
        )
        org = Organisation.objects.create(name="John's Organisation")
        org.users.add(user)

        self.client.force_authenticate(user=user)
        url = reverse('user-detail', args=[user.userId])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'john@example.com')

    def test_organisation_list_access(self):
        user = User.objects.create_user(
            email='john@example.com',
            firstName='John',
            lastName='Doe',
            password='password123'
        )
        org = Organisation.objects.create(name="John's Organisation")
        org.users.add(user)

        self.client.force_authenticate(user=user)
        url = reverse('organisation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['organisations'][0]['name'], "John's Organisation")

    def test_organisation_access_restriction(self):
        user1 = User.objects.create_user(
            email='john@example.com',
            firstName='John',
            lastName='Doe',
            password='password123'
        )
        user2 = User.objects.create_user(
            email='jane@example.com',
            firstName='Jane',
            lastName='Doe',
            password='password123'
        )
        org = Organisation.objects.create(name="John's Organisation")
        org.users.add(user1)

        self.client.force_authenticate(user=user2)
        url = reverse('organisation-detail', args=[org.org_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
