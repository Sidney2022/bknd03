
from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('api-auth/', include('rest_framework.urls')),  
]

