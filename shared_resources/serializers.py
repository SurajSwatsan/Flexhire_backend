from rest_framework import serializers
from .models import Country, CasteCategory, State, University, Course, Specialization


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = State
        fields = ["id", "name", "country"]


class CasteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CasteCategory
        fields = ["id", "name"]


class UniversitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = University
        fields = ["id", "name", "state"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name"]


class SpecializationSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Nested serializer for the related course

    class Meta:
        model = Specialization
        fields = ["id", "name", "course"]
