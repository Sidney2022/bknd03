
import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from accounts.models import Organisation, User

User = get_user_model()

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_registration_success(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': '1234test',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Registration successful')
    
    def test_access_token_generation(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': '1234test',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['message'], 'Registration successful')
    
    def test_registration_missing_fields(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)
    
    def test_registration_existing_email(self):
        User.objects.create(
            firstName='Jane',
            lastName='Doe',
            email='jane.doe@example.com',
            password='1234test'
        )
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'jane.doe@example.com',
            'password': '1234test',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)

    def test_default_organisation_created(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': '1234test',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=data['email'])
        org = Organisation.objects.get(users=user)
        self.assertEqual(org.name, f"{data['firstName']}'s Organisation")

if __name__ == '__main__':
    unittest.main()

#         sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#         from accounts.views import RegisterView
#         sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#         from rest_framework.test import APIRequestFactory
#         sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#         from accounts.models import User, Organisation

#         # Mock the UserSerializer to be valid and return a user instance
#         mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
#         mock_user = mocker.Mock(spec=User)
#         mock_serializer.return_value.is_valid.return_value = True
#         mock_serializer.return_value.save.return_value = mock_user

#         # Mock the user instance methods and attributes
#         mock_user.set_password = mocker.Mock()
#         mock_user.save = mocker.Mock()
#         mock_user.firstName = "Alice"
#         mock_user.lastName = "Smith"
#         mock_user.email = "alice.smith@example.com"
#         mock_user.phone = "9876543210"
#         mock_user.userId = 2

#         # Mock the Organisation model's create method
#         mock_organisation = mocker.Mock(spec=Organisation)
#         mocker.patch('accounts.models.Organisation.objects.create', return_value=mock_organisation)

#         # Mock the RefreshToken for user
#         mock_refresh_token = mocker.Mock()
#         mock_refresh_token.access_token = "mock_access_token"
#         mocker.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user', return_value=mock_refresh_token)

#         # Create a request with valid data
#         factory = APIRequestFactory()
#         request = factory.post('/register', {
#             'firstName': 'Alice',
#             'lastName': 'Smith',
#             'email': 'alice.smith@example.com',
#             'phone': '9876543210',
#             'password': 'securepassword'
#         })

#         # Call the view
#         view = RegisterView.as_view()
#         response = view(request)

#         # Assert the response status and data
#         assert response.status_code == 201
#         assert response.data['status'] == 'success'
#         assert response.data['message'] == 'Registration successful'
#         assert response.data['data']['accessToken'] == "mock_access_token"
#         assert response.data['data']['user']['firstName'] == "Alice"