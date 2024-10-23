from django.urls import path
from .views import (
    JobSeekerDetail,
    CareerPreferencesDetail,
    BasicDetailsDetail,
    ResumeVideoProfileDetail,
    ProfessionalDetailsDetail,
    EmploymentDetail,
    ProjectDetail,
    ITSkillDetail,
    EducationDetail,
    AccomplishmentDetail,
    PersonalDetailDetail,
    LanguageDetail,
    JobSeekerDetailWithRelations,
)

urlpatterns = [
    path("jobseekers", JobSeekerDetail.as_view(), name="jobseeker-list"),
    path("jobseekers/<int:pk>", JobSeekerDetail.as_view(), name="jobseeker-detail"),
    path("career-preferences", CareerPreferencesDetail.as_view()),
    path("career-preferences/<int:job_seeker_id>", CareerPreferencesDetail.as_view()),
    path("basic-details", BasicDetailsDetail.as_view(), name="basic-details-list"),
    path("basic-details/<int:job_seeker_id>", BasicDetailsDetail.as_view()),
    path("resume-video-profile/", ResumeVideoProfileDetail.as_view()),
    path("resume-video-profile/<int:job_seeker_id>/", ResumeVideoProfileDetail.as_view()),
    path("professional-details", ProfessionalDetailsDetail.as_view()),
    path("professional-details/<int:job_seeker_id>", ProfessionalDetailsDetail.as_view()),
    path("employment", EmploymentDetail.as_view(), name="employment-list"),
    path("employment/<int:pk>", EmploymentDetail.as_view(), name="employment-detail"),
    path("projects", ProjectDetail.as_view(), name="project-list"),
    path("projects/<int:pk>", ProjectDetail.as_view(), name="project-detail"),
    path("it-skills", ITSkillDetail.as_view(), name="it-skill-list"),
    path("it-skills/<int:pk>", ITSkillDetail.as_view(), name="it-skill-detail"),
    path("education", EducationDetail.as_view(), name="education-list"),
    path("education/<int:pk>", EducationDetail.as_view(), name="education-detail"),
    path("accomplishments", AccomplishmentDetail.as_view(), name="accomplishment-list"),
    path("accomplishments/<int:pk>", AccomplishmentDetail.as_view()),
    path("personal-details", PersonalDetailDetail.as_view(), name="personal-detail-list"),
    path("personal-details/<int:job_seeker_id>", PersonalDetailDetail.as_view()),
    path("languages", LanguageDetail.as_view(), name="language-list"),
    path("languages/<int:pk>", LanguageDetail.as_view(), name="language-detail"),
    path("jobseeker-detail/<int:user_id>", JobSeekerDetailWithRelations.as_view()),
]
