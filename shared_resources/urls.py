from django.urls import path
from .views import CountryAPIView, CountryByRegionAPIView, DistinctRegionAPIView

urlpatterns = [
    path('countries', CountryAPIView.as_view()),
    path('countries/region/<str:region>', CountryByRegionAPIView.as_view(), name='country-by-region'),
    path('countries/regions', DistinctRegionAPIView.as_view(), name='distinct-regions'),
]
