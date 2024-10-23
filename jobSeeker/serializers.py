from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
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


class JobSeekerSerializer(serializers.ModelSerializer):
    profile_photo = Base64ImageField(required=False)

    class Meta:
        model = JobSeeker
        fields = "__all__"


class CareerPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPreferences
        fields = "__all__"


class BasicDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicDetails
        fields = "__all__"


class ResumeVideoProfileSerializer(serializers.ModelSerializer):
    # resume = Base64ImageField(required=False)
    # video_profile = Base64ImageField(required=False)

    class Meta:
        model = ResumeVideoProfile
        fields = "__all__"


class ProfessionalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalDetails
        fields = "__all__"


class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ITSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITSkill
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class AccomplishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accomplishment
        fields = "__all__"


class PersonalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetail
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class JobSeekerDetailSerializer(serializers.ModelSerializer):
    career_preferences = CareerPreferencesSerializer(read_only=True)
    basic_details = BasicDetailsSerializer(read_only=True)
    resume_video_profile = ResumeVideoProfileSerializer(read_only=True)
    professional_details = ProfessionalDetailsSerializer(read_only=True)
    employments = EmploymentSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    it_skills = ITSkillSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    accomplishments = AccomplishmentSerializer(many=True, read_only=True)
    personal_details = PersonalDetailSerializer(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = JobSeeker
        fields = [
            "id",
            "user_id",
            "full_name",
            "profile_photo",
            "profile_headline",
            "career_preferences",
            "basic_details",
            "resume_video_profile",
            "professional_details",
            "employments",
            "projects",
            "it_skills",
            "education",
            "accomplishments",
            "personal_details",
            "languages",
        ]
