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


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = User.objects.get(userId=id)
        if user:
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
        return Response({"status": "Bad request", "message": "User not found", "statusCode": 404})


class OrganisationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        return self.request.user.organisations.all()


# class OrganisationDetailView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrganisationSerializer
#     lookup_field = 'org_id'
#     queryset = Organisation.objects.all()

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Organisation
from .serializers import OrganisationSerializer
from rest_framework.exceptions import PermissionDenied

class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, org_id):
        organisation = Organisation.objects.get(org_id=org_id)
        if request.user not in organisation.users.all():
            raise PermissionDenied("You do not have access to this organisation.")
        serializer = OrganisationSerializer(organisation)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class CreateOrganisationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer

    def perform_create(self, serializer):
        organisation = serializer.save()
        organisation.users.add(self.request.user)

