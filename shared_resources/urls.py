from django.urls import path
from .views import (
    CountryAPIView,
    CountryByRegionAPIView,
    DistinctRegionAPIView,
    CasteCategoryDetail,
    StateList,
    UniversityList,
    CourseList,
)

urlpatterns = [
    path("countries", CountryAPIView.as_view()),
    path("countries/region/<str:region>", CountryByRegionAPIView.as_view()),
    path("countries/regions", DistinctRegionAPIView.as_view(), name="distinct-regions"),
    path("caste-categories", CasteCategoryDetail.as_view(), name="caste-category-list"),
    path("caste-categories/<int:pk>", CasteCategoryDetail.as_view()),
    path("states", StateList.as_view(), name="state-list"),
    path("universities", UniversityList.as_view(), name="university-list"),
    path("courses", CourseList.as_view(), name="course-list"),
]
