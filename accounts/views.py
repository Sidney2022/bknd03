from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Organisation
from .serializers import OrganisationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()

            org_name = f"{user.firstName}'s Organisation"
            organisation = Organisation.objects.create(name=org_name)
            organisation.users.add(user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": access_token,
                    "user": {
                        "userId": str(user.userId),
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

         # Handle validation errors
        errors = [{"field": key, "message": str(value[0])} for key, value in serializer.errors.items()]
        return Response({"errors": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user': {
            'userId': self.user.userId,
            'firstName': self.user.firstName,
            'lastName': self.user.lastName,
            'email': self.user.email,
            'phone': self.user.phone,
        }})
        return data


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": access_token,
                    "user": {
                        "userId": str(user.userId),
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"status": "Bad request", "message": "Authentication failed", "statusCode": 401})


class AddUserToOrganisationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        # Retrieve the organization
        try:
            organisation = Organisation.objects.get(org_id=org_id)
        except Organisation.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('userId')
        try:
            user = User.objects.get(userId=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user in organisation.users.all():
            return Response({'error': 'User is already a member of this organization'}, status=status.HTTP_400_BAD_REQUEST)

        organisation.users.add(user)

        return Response({
            'status': 'success',
            'message': 'User added to organization successfully'
        }, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Retrieve the authenticated user from the request
        requesting_user = request.user

        try:
            # Retrieve the user by the ID passed in the URL
            user = User.objects.get(userId=id)
        except User.DoesNotExist:
            return Response({"status": "Bad request", "message": "User not found", "statusCode": 404})

        # Check if the authenticated user's ID matches the ID in the URL
        if requesting_user.userId == id:
            response_data = {
                "status": "success",
                "message": "User record retrieved",
                "data": {
                    "userId": str(user.userId),
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # Check if both users belong to the same organization
        user_organisations = Organisation.objects.filter(users=user)
        requesting_user_organisations = Organisation.objects.filter(users=requesting_user)

        if user_organisations.intersection(requesting_user_organisations).exists():
            response_data = {
                "status": "success",
                "message": "User record retrieved",
                "data": {
                    "userId": str(user.userId),
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # If none of the above conditions are met, return a forbidden response
        return Response({"status": "Forbidden", "message": "You do not have permission to access this user's details", "statusCode": 403})


class OrganisationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        return self.request.user.organisations.all()


class OrganisationView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        return self.request.user.organisations.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            description = serializer.validated_data.get('description')

            # Check if an organization with the same name exists for the current user
            existing_org = Organisation.objects.filter(name=name, users=request.user).first()
            if existing_org:
                # Return existing organization with the same schema as if it was created
                serializer = OrganisationSerializer(existing_org)
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)

            # Create the organisation
            organisation = Organisation.objects.create(name=name, description=description)
            organisation.users.add(request.user)

            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AvailableEndPoints(APIView):
    def get(self, request):
        response = {
            f"Register --  / POST /" : "/auth/register",
            f"Login --  / POST /" : "/auth/login",
            f"Organisations List --  / GET /" : "/api/organisations",
            f"Single Organisation --  / GET /" : "/api/organisations/<org_id>",
            f"Create Organisation --  / POST /" : "/api/organisations/<org_id>/users",

        }
        return Response(response)