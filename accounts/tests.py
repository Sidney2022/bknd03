# tests/test_user_registration.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.invalid_payloads = [
            {
                "firstName": "",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "password": "password123",
                "phone": "1234567890"
            },
            {
                "firstName": "John",
                "lastName": "",
                "email": "john.doe@example.com",
                "password": "password123",
                "phone": "1234567890"
            },
            {
                "firstName": "John",
                "lastName": "Doe",
                "email": "",
                "password": "password123",
                "phone": "1234567890"
            },
            {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "password": "",
                "phone": "1234567890"
            }
        ]

    def test_register_user_success(self):
        response = self.client.post('/auth/register', data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('user', response.data['data'])

    def test_register_user_missing_fields(self):
        for payload in self.invalid_payloads:
            response = self.client.post('/auth/register', data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
            self.assertIn('errors', response.data)

    def test_register_user_duplicate_email(self):
        self.client.post('/auth/register', data=self.valid_payload, format='json')
        response = self.client.post('/auth/register', data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)
