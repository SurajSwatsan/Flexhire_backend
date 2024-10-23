from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    JobSeeker,
    CareerPreferences,
    BasicDetails,
    ResumeVideoProfile,
    ProfessionalDetails,
    Employment,
    Project,
    ITSkill,
    Education,
    Accomplishment,
    PersonalDetail,
    Language,
)
from .serializers import (
    JobSeekerSerializer,
    CareerPreferencesSerializer,
    BasicDetailsSerializer,
    ResumeVideoProfileSerializer,
    ProfessionalDetailsSerializer,
    EmploymentSerializer,
    ProjectSerializer,
    ITSkillSerializer,
    EducationSerializer,
    AccomplishmentSerializer,
    PersonalDetailSerializer,
    LanguageSerializer,
    JobSeekerDetailSerializer,
)


# JobSeeker API
class JobSeekerDetail(APIView):
    def get(self, request, pk=None):
        if pk:
            job_seeker = JobSeeker.objects.get(pk=pk)
            if job_seeker is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = JobSeekerSerializer(job_seeker)
            return Response(serializer.data)
        job_seekers = JobSeeker.objects.all()
        serializer = JobSeekerSerializer(job_seekers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSeekerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        job_seeker = JobSeeker.objects.get(pk=pk)
        if job_seeker is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JobSeekerSerializer(job_seeker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job_seeker = JobSeeker.objects.get(pk=pk)
        if job_seeker is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        job_seeker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Career Preferences API


class CareerPreferencesDetail(APIView):

    def get(self, request, job_seeker_id=None):
        if job_seeker_id:
            career_preferences = CareerPreferences.objects.get(
                job_seeker__id=job_seeker_id
            )
            if career_preferences is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CareerPreferencesSerializer(career_preferences)
            return Response(serializer.data)
        career_preferences = CareerPreferences.objects.all()
        serializer = CareerPreferencesSerializer(career_preferences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CareerPreferencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_seeker_id):
        career_preferences = CareerPreferences.objects.get(job_seeker__id=job_seeker_id)
        if career_preferences is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CareerPreferencesSerializer(career_preferences, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_seeker_id):
        career_preferences = CareerPreferences.objects.get(job_seeker__id=job_seeker_id)
        if career_preferences is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        career_preferences.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Basic Details API


class BasicDetailsDetail(APIView):

    def get(self, request, job_seeker_id):
        if job_seeker_id:
            basic_details = BasicDetails.objects.get(job_seeker__id=job_seeker_id)
            if basic_details is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = BasicDetailsSerializer(basic_details)
            return Response(serializer.data)
        basic_details = BasicDetails.objects.all()
        serializer = BasicDetailsSerializer(basic_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BasicDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_seeker_id):
        basic_details = BasicDetails.objects.get(job_seeker__id=job_seeker_id)
        if basic_details is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BasicDetailsSerializer(basic_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_seeker_id):
        basic_details = BasicDetails.objects.get(job_seeker__id=job_seeker_id)
        if basic_details is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        basic_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Resume and Video Profile API
class ResumeVideoProfileDetail(APIView):
    def get(self, request, job_seeker_id):
        resume_video_profile = ResumeVideoProfile.objects.get(
            job_seeker__id=job_seeker_id
        )
        if resume_video_profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ResumeVideoProfileSerializer(resume_video_profile)
        return Response(serializer.data)

    def post(self, request):
        # if 'video' in request.FILES and 'title' in request.POST:
        #     job_seeker = request.POST['job_seeker']
        #     resume = request.FILES['resume']
        #     video_profile = request.FILES['video_profile']
        #     context={
        #         "job_seeker":job_seeker,
        #         "resume":resume,
        #         "video_profile":video_profile
        #     }
        # Get the title from the form
        serializer = ResumeVideoProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_seeker_id):
        resume_video_profile = ResumeVideoProfile.objects.get(
            job_seeker__id=job_seeker_id
        )
        if resume_video_profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ResumeVideoProfileSerializer(
            resume_video_profile, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_seeker_id):
        resume_video_profile = ResumeVideoProfile.objects.get(
            job_seeker__id=job_seeker_id
        )
        if resume_video_profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        resume_video_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Professional Details API


class ProfessionalDetailsDetail(APIView):

    def get(self, request, job_seeker_id):
        if job_seeker_id:
            professional_details = ProfessionalDetails.objects.get(
                job_seeker__id=job_seeker_id
            )
            if professional_details is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProfessionalDetailsSerializer(professional_details)
            return Response(serializer.data)
        professional_details = ProfessionalDetails.objects.all()
        serializer = ProfessionalDetailsSerializer(professional_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfessionalDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_seeker_id):
        professional_details = ProfessionalDetails.objects.get(
            job_seeker__id=job_seeker_id
        )
        if professional_details is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProfessionalDetailsSerializer(
            professional_details, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_seeker_id):
        professional_details = ProfessionalDetails.objects.get(
            job_seeker__id=job_seeker_id
        )
        if professional_details is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        professional_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Employment API


class EmploymentDetail(APIView):

    def get(self, request, pk=None):
        if pk:
            employment = Employment.objects.get(pk=pk)
            if employment is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = EmploymentSerializer(employment)
            return Response(serializer.data)
        employments = Employment.objects.all()
        serializer = EmploymentSerializer(employments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmploymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        employment = Employment.objects.get(pk=pk)
        if employment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmploymentSerializer(employment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employment = Employment.objects.get(pk=pk)
        if employment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        employment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Project API


class ProjectDetail(APIView):

    def get(self, request, pk=None):
        if pk:
            project = Project.objects.get(pk=pk)
            if project is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        project = Project.objects.get(pk=pk)
        if project is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = Project.objects.get(pk=pk)
        if project is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# IT Skills API


class ITSkillDetail(APIView):

    def get(self, request, pk=None):
        if pk:
            it_skill = ITSkill.objects.get(pk=pk)
            if it_skill is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ITSkillSerializer(it_skill)
            return Response(serializer.data)
        it_skills = ITSkill.objects.all()
        serializer = ITSkillSerializer(it_skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ITSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        it_skill = ITSkill.objects.get(pk=pk)
        if it_skill is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ITSkillSerializer(it_skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        it_skill = ITSkill.objects.get(pk=pk)
        if it_skill is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        it_skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Education API


class EducationDetail(APIView):

    def get(self, request, pk=None):
        if pk:
            education = Education.objects.get(pk=pk)
            if education is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = EducationSerializer(education)
            return Response(serializer.data)
        education = Education.objects.all()
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        education = Education.objects.get(pk=pk)
        if education is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        education = Education.objects.get(pk=pk)
        if education is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Accomplishments API


class AccomplishmentDetail(APIView):

    def get(self, request, pk=None):
        if pk:
            accomplishment = Accomplishment.objects.get(pk=pk)
            if accomplishment is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = AccomplishmentSerializer(accomplishment)
            return Response(serializer.data)
        accomplishments = Accomplishment.objects.all()
        serializer = AccomplishmentSerializer(accomplishments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccomplishmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        accomplishment = Accomplishment.objects.get(pk=pk)
        if accomplishment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AccomplishmentSerializer(accomplishment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        accomplishment = Accomplishment.objects.get(pk=pk)
        if accomplishment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        accomplishment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Personal Details API


class PersonalDetailDetail(APIView):

    def get(self, request, job_seeker_id=None):
        if job_seeker_id:
            personal_detail = PersonalDetail.objects.get(job_seeker__id=job_seeker_id)
            if personal_detail is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = PersonalDetailSerializer(personal_detail)
            return Response(serializer.data)
        personal_details = PersonalDetail.objects.all()
        serializer = PersonalDetailSerializer(personal_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonalDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_seeker_id):
        personal_detail = PersonalDetail.objects.get(job_seeker__id=job_seeker_id)
        if personal_detail is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalDetailSerializer(personal_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_seeker_id):
        personal_detail = PersonalDetail.objects.get(job_seeker__id=job_seeker_id)
        if personal_detail is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        personal_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Language API


class LanguageDetail(APIView):

    def get(self, request, pk=None):
        if pk:
            language = Language.objects.get(pk=pk)
            if language is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = LanguageSerializer(language)
            return Response(serializer.data)
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        language = Language.objects.get(pk=pk)
        if language is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LanguageSerializer(language, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        language = Language.objects.get(pk=pk)
        if language is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobSeekerDetailWithRelations(APIView):
    def get(self, request, user_id):
        try:
            job_seeker = JobSeeker.objects.get(user_id=user_id)

            data = JobSeekerDetailSerializer(job_seeker).data
            return Response(data, status=status.HTTP_200_OK)

        except JobSeeker.DoesNotExist:
            return Response(
                {"error": "Job seeker not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
