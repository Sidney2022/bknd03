from django.urls import path
from . import views

urlpatterns = [
    path('auth/register', views.RegisterView.as_view(), ),
    path('auth/login', views.LoginView.as_view(), ),
    path('organisations', views.OrganisationView.as_view(), name='organisation-view'),
    path('organisations/<str:org_id>/users', views.AddUserToOrganisationView.as_view(), name='organisation-add-user'),

    path('users/<str:id>', views.UserDetailView.as_view(), name='user-detail'),

]
