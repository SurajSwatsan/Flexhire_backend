from django.urls import path
from .views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    PasswordResetAPIView,
    SetNewPasswordAPIView,
    SocialMediaLoginAPIView,
    RoleListCreateAPIView,
    RoleDetailAPIView,
    CustomerAdminRegistrationAPIView
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('social-media-login/', SocialMediaLoginAPIView.as_view(), name='social-media-login'),
    path('password-reset/', PasswordResetAPIView.as_view(), name='password-reset'),
    path('set-new-password/', SetNewPasswordAPIView.as_view(), name='set-new-password'),
    path('roles/', RoleListCreateAPIView.as_view(), name='role-list-create'),  # List and create roles
    path('roles/<int:pk>/', RoleDetailAPIView.as_view(), name='role-detail'),  # Retrieve, update, delete role
    path('register-customer-admin/', CustomerAdminRegistrationAPIView.as_view(), name='register-customer-admin'),  # New endpoint

]
