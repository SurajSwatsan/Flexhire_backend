# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmployerProfile
from .serializers import EmployerProfileSerializer,GetEmployerProfileSerializer

class EmployerCreateAPIView(APIView):
    def post(self, request):
        serializer = EmployerProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployerDetailAPIView(APIView):
    def get(self, request, employer_id):
        try:
            profile = EmployerProfile.objects.get(employer_id=employer_id)
            serializer = GetEmployerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Employer profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, employer_id):
        try:
            profile = EmployerProfile.objects.get(employer_id=employer_id)
            serializer = EmployerProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Employer profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, employer_id):
        try:
            profile = EmployerProfile.objects.get(employer_id=employer_id)
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Employer profile not found'}, status=status.HTTP_404_NOT_FOUND)

class EmployerProfileDetailView(APIView):
    def get_object(self, employer_id):
        try:
            return EmployerProfile.objects.get(employer_id=employer_id)
        except EmployerProfile.DoesNotExist:
            return None

    def get(self, request, employer_id):
        profile = self.get_object(employer_id)
        if profile is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GetEmployerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)