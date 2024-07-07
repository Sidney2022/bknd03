from django.urls import path
from . import views

urlpatterns = [
    # path('/register', views.RegisterView.as_view(), name='register'),
    # path('auth/login', views.LoginView.as_view(), name='login'),
    path('users/<str:id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('organisations', views.OrganisationListView.as_view(), name='organisation-list'),
    path('organisations/<str:org_id>', views.OrganisationDetailView.as_view(), name='organisation-detail'),
    path('organisations/<str:org_id>/users', views.CreateOrganisationView.as_view(), name='create-organisation'),
]
