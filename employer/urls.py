# urls.py

from django.urls import path
from .views import EmployerCreateAPIView, EmployerDetailAPIView,EmployerProfileDetailView

urlpatterns = [
    path('employers/create/', EmployerCreateAPIView.as_view()),
    path('employers/<int:employer_id>/', EmployerDetailAPIView.as_view()),
    path('employer-profiles/<int:employer_id>/', EmployerProfileDetailView.as_view()),

]
