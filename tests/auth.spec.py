import os
import sys
import pytest

# Ensure the parent directory is in the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Dependencies:
# pip install pytest-mock


@pytest.mark.django_db
class TestRegisterView:

    # Successful registration with valid data
    def test_successful_registration_with_valid_data(self, mocker):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.views import RegisterView
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from rest_framework.test import APIRequestFactory
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.models import User, Organisation

        # Mock the UserSerializer to always be valid and return a user instance
        mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
        mock_user = mocker.Mock(spec=User)
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = mock_user

        # Mock the user instance methods and attributes
        mock_user.set_password = mocker.Mock()
        mock_user.save = mocker.Mock()
        mock_user.firstName = "John"
        mock_user.lastName = "Doe"
        mock_user.email = "john.doe@example.com"
        mock_user.phone = "1234567890"
        mock_user.userId = 1

        # Mock the Organisation model's create method
        mock_organisation = mocker.Mock(spec=Organisation)
        mocker.patch('accounts.models.Organisation.objects.create', return_value=mock_organisation)

        # Mock the RefreshToken for user
        mock_refresh_token = mocker.Mock()
        mock_refresh_token.access_token = "mock_access_token"
        mocker.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user', return_value=mock_refresh_token)

        # Create a request with valid data
        factory = APIRequestFactory()
        request = factory.post('/register', {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'password': 'password123'
        })

        # Call the view
        view = RegisterView.as_view()
        response = view(request)

        # Assert the response status and data
        assert response.status_code == 201
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'Registration successful'
        assert response.data['data']['accessToken'] == "mock_access_token"
        assert response.data['data']['user']['firstName'] == "John"

    # Registration with missing required fields
    def test_registration_with_missing_required_fields(self, mocker):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.views import RegisterView
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from rest_framework.test import APIRequestFactory

        # Mock the UserSerializer to be invalid and return errors
        mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'firstName': ['This field is required.'],
            'email': ['This field is required.']
        }

        # Create a request with missing required fields
        factory = APIRequestFactory()
        request = factory.post('/register', {
            'lastName': 'Doe',
            'phone': '1234567890',
            'password': 'password123'
        })

        # Call the view
        view = RegisterView.as_view()
        response = view(request)

        # Assert the response status and data
        assert response.status_code == 422
        assert response.data['errors'] == [
            {'field': 'firstName', 'message': 'This field is required.'},
            {'field': 'email', 'message': 'This field is required.'}
        ]

    # Access token is generated and returned in response
    def test_access_token_generated_and_returned(self, mocker):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.views import RegisterView
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from rest_framework.test import APIRequestFactory
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.models import User, Organisation

        # Mock the UserSerializer to be valid and return a user instance
        mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
        mock_user = mocker.Mock(spec=User)
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = mock_user

        # Mock the user instance methods and attributes
        mock_user.set_password = mocker.Mock()
        mock_user.save = mocker.Mock()
        mock_user.firstName = "John"
        mock_user.lastName = "Doe"
        mock_user.email = "john.doe@example.com"
        mock_user.phone = "1234567890"
        mock_user.userId = 1

        # Mock the Organisation model's create method
        mock_organisation = mocker.Mock(spec=Organisation)
        mocker.patch('accounts.models.Organisation.objects.create', return_value=mock_organisation)

        # Mock the RefreshToken for user
        mock_refresh_token = mocker.Mock()
        mock_refresh_token.access_token = "mock_access_token"
        mocker.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user', return_value=mock_refresh_token)

        # Create a request with valid data
        factory = APIRequestFactory()
        request = factory.post('/register', {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'password': 'password123'
        })

        # Call the view
        view = RegisterView.as_view()
        response = view(request)

        # Assert the response status and data
        assert response.status_code == 201
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'Registration successful'
        assert response.data['data']['accessToken'] == "mock_access_token"
        assert response.data['data']['user']['firstName'] == "John"

    # Organisation is created with the correct name
    def test_organisation_created_with_correct_name(self, mocker):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.views import RegisterView
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from rest_framework.test import APIRequestFactory
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.models import User, Organisation

        # Mock the UserSerializer to be valid and return a user instance
        mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
        mock_user = mocker.Mock(spec=User)
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = mock_user

        # Mock the user instance methods and attributes
        mock_user.set_password = mocker.Mock()
        mock_user.save = mocker.Mock()
        mock_user.firstName = "John"
        mock_user.lastName = "Doe"
        mock_user.email = "john.doe@example.com"
        mock_user.phone = "1234567890"
        mock_user.userId = 1

        # Mock the Organisation model's create method
        mock_organisation = mocker.Mock(spec=Organisation)
        mocker.patch('accounts.models.Organisation.objects.create', return_value=mock_organisation)

        # Mock the RefreshToken for user
        mock_refresh_token = mocker.Mock()
        mock_refresh_token.access_token = "mock_access_token"
        mocker.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user', return_value=mock_refresh_token)

        # Create a request with valid data
        factory = APIRequestFactory()
        request = factory.post('/register', {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'password': 'password123'
        })

        # Call the view
        view = RegisterView.as_view()
        response = view(request)

        # Assert the response status and data
        assert response.status_code == 201
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'Registration successful'
        assert response.data['data']['accessToken'] == "mock_access_token"
        assert response.data['data']['user']['firstName'] == "John"

    # Verify access token is present in response data
    def test_verify_access_token_in_response_data(self, mocker):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.views import RegisterView
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from rest_framework.test import APIRequestFactory
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.models import User, Organisation

        # Mock the UserSerializer to always be valid and return a user instance
        mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
        mock_user = mocker.Mock(spec=User)
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = mock_user

        # Mock the user instance methods and attributes
        mock_user.set_password = mocker.Mock()
        mock_user.save = mocker.Mock()
        mock_user.firstName = "John"
        mock_user.lastName = "Doe"
        mock_user.email = "john.doe@example.com"
        mock_user.phone = "1234567890"
        mock_user.userId = 1

        # Mock the Organisation model's create method
        mock_organisation = mocker.Mock(spec=Organisation)
        mocker.patch('accounts.models.Organisation.objects.create', return_value=mock_organisation)

        # Mock the RefreshToken for user
        mock_refresh_token = mocker.Mock()
        mock_refresh_token.access_token = "mock_access_token"
        mocker.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user', return_value=mock_refresh_token)

        # Create a request with valid data
        factory = APIRequestFactory()
        request = factory.post('/register', {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'password': 'password123'
        })

        # Call the view
        view = RegisterView.as_view()
        response = view(request)

        # Assert the response status and data
        assert response.status_code == 201
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'Registration successful'
        assert response.data['data']['accessToken'] == "mock_access_token"
        assert response.data['data']['user']['firstName'] == "John"

    # User password is set correctly
    def test_user_password_set_correctly(self, mocker):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.views import RegisterView
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from rest_framework.test import APIRequestFactory
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.models import User, Organisation

        # Mock the UserSerializer to be valid and return a user instance
        mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
        mock_user = mocker.Mock(spec=User)
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = mock_user

        # Mock the user instance methods and attributes
        mock_user.set_password = mocker.Mock()
        mock_user.save = mocker.Mock()
        mock_user.firstName = "Alice"
        mock_user.lastName = "Smith"
        mock_user.email = "alice.smith@example.com"
        mock_user.phone = "9876543210"
        mock_user.userId = 2

        # Mock the Organisation model's create method
        mock_organisation = mocker.Mock(spec=Organisation)
        mocker.patch('accounts.models.Organisation.objects.create', return_value=mock_organisation)

        # Mock the RefreshToken for user
        mock_refresh_token = mocker.Mock()
        mock_refresh_token.access_token = "mock_access_token"
        mocker.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user', return_value=mock_refresh_token)

        # Create a request with valid data
        factory = APIRequestFactory()
        request = factory.post('/register', {
            'firstName': 'Alice',
            'lastName': 'Smith',
            'email': 'alice.smith@example.com',
            'phone': '9876543210',
            'password': 'securepassword123'
        })

        # Call the view
        view = RegisterView.as_view()
        response = view(request)

        # Assert the response status and data
        assert response.status_code == 201
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'Registration successful'
        assert response.data['data']['accessToken'] == "mock_access_token"
        assert response.data['data']['user']['firstName'] == "Alice"

    # Validate response status code is 201
    def test_validate_response_status_code_201(self, mocker):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.views import RegisterView
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from rest_framework.test import APIRequestFactory
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.models import User, Organisation

        # Mock the UserSerializer to always be valid and return a user instance
        mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
        mock_user = mocker.Mock(spec=User)
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = mock_user

        # Mock the user instance methods and attributes
        mock_user.set_password = mocker.Mock()
        mock_user.save = mocker.Mock()
        mock_user.firstName = "Alice"
        mock_user.lastName = "Smith"
        mock_user.email = "alice.smith@example.com"
        mock_user.phone = "9876543210"
        mock_user.userId = 2

        # Mock the Organisation model's create method
        mock_organisation = mocker.Mock(spec=Organisation)
        mocker.patch('accounts.models.Organisation.objects.create', return_value=mock_organisation)

        # Mock the RefreshToken for user
        mock_refresh_token = mocker.Mock()
        mock_refresh_token.access_token = "mock_access_token"
        mocker.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user', return_value=mock_refresh_token)

        # Create a request with valid data
        factory = APIRequestFactory()
        request = factory.post('/register', {
            'firstName': 'Alice',
            'lastName': 'Smith',
            'email': 'alice.smith@example.com',
            'phone': '9876543210',
            'password': 'password123'
        })

        # Call the view
        view = RegisterView.as_view()
        response = view(request)

        # Assert the response status and data
        assert response.status_code == 201
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'Registration successful'
        assert response.data['data']['accessToken'] == "mock_access_token"
        assert response.data['data']['user']['firstName'] == "Alice"

    # User is added to the organisation
    def test_user_added_to_organisation(self, mocker):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.views import RegisterView
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from rest_framework.test import APIRequestFactory
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from accounts.models import User, Organisation

        # Mock the UserSerializer to be valid and return a user instance
        mock_serializer = mocker.patch('accounts.serializers.UserSerializer')
        mock_user = mocker.Mock(spec=User)
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = mock_user

        # Mock the user instance methods and attributes
        mock_user.set_password = mocker.Mock()
        mock_user.save = mocker.Mock()
        mock_user.firstName = "Alice"
        mock_user.lastName = "Smith"
        mock_user.email = "alice.smith@example.com"
        mock_user.phone = "9876543210"
        mock_user.userId = 2

        # Mock the Organisation model's create method
        mock_organisation = mocker.Mock(spec=Organisation)
        mocker.patch('accounts.models.Organisation.objects.create', return_value=mock_organisation)

        # Mock the RefreshToken for user
        mock_refresh_token = mocker.Mock()
        mock_refresh_token.access_token = "mock_access_token"
        mocker.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user', return_value=mock_refresh_token)

        # Create a request with valid data
        factory = APIRequestFactory()
        request = factory.post('/register', {
            'firstName': 'Alice',
            'lastName': 'Smith',
            'email': 'alice.smith@example.com',
            'phone': '9876543210',
            'password': 'securepassword'
        })

        # Call the view
        view = RegisterView.as_view()
        response = view(request)

        # Assert the response status and data
        assert response.status_code == 201
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'Registration successful'
        assert response.data['data']['accessToken'] == "mock_access_token"
        assert response.data['data']['user']['firstName'] == "Alice"