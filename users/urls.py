from django.urls import path
from rest_framework.authtoken import views
from .views import UserProfileView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('token/', views.obtain_auth_token, name='api-token-auth'),
]
