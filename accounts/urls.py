from django.urls import path
from .views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    PasswordResetAPIView,
    SetNewPasswordAPIView,
    SocialMediaLoginAPIView,
    RolesAPIView,
    CustomerAdminRegistrationAPIView,AdminRegistrationAPIView
)

urlpatterns = [
    path('roles/', RolesAPIView.as_view()),
    path('roles/<int:pk>/', RolesAPIView.as_view()),
    path('register-admin/', AdminRegistrationAPIView.as_view(), name='register-admin'),  
    path('register-customer-admin/', CustomerAdminRegistrationAPIView.as_view(), name='register-customer-admin'),  
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('social-media-login/', SocialMediaLoginAPIView.as_view(), name='social-media-login'),
    path('password-reset/', PasswordResetAPIView.as_view(), name='password-reset'),
    path('set-new-password/', SetNewPasswordAPIView.as_view(), name='set-new-password'),
]
