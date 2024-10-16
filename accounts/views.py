from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserMaster, RoleMaster
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    PasswordResetSerializer,
    SetNewPasswordSerializer,
    SocialMediaLoginSerializer,
    RoleSerializer,
    CustomerAdminRegistrationSerializer,
    AdminRegistrationSerializer,
    AdminTeamRegistrationSerializer,
    CustomerTeamRegistrationSerializer,
)
from django.http import Http404
from .permissions import IsAdminUser, IsCustomerUser
from rest_framework.permissions import IsAuthenticated


class RolesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            # Check if the requesting user is an admin
            if self.request.user.user_type.role_name != "Employer":
                return Response(
                    {"detail": "Only customer admins can access data"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            roles = RoleMaster.objects.filter(parent=pk)
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Check if the requesting user is an admin
        if self.request.user.user_type.role_name != "Admin":
            return Response(
                {"detail": "Only admins can access data"},
                status=status.HTTP_403_FORBIDDEN,
            )

        roles = RoleMaster.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Check if the requesting user is an admin
        if self.request.user.user_type.role_name != "Admin":
            return Response(
                {"detail": "Only admins can add a role"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Role created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Check if the requesting user is an admin
        if self.request.user.user_type.role_name != "Admin":
            return Response(
                {"detail": "Only admins can update a role"},
                status=status.HTTP_403_FORBIDDEN,
            )
        role = RoleMaster.objects.get(id=pk)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Role updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Check if the requesting user is an admin
        if self.request.user.user_type.role_name != "Admin":
            return Response(
                {"detail": "Only admins can delete a role"},
                status=status.HTTP_403_FORBIDDEN,
            )
        role = RoleMaster.objects.get(id=pk)
        role.delete()
        return Response(
            {"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class AdminRegistrationAPIView(APIView):
    # permission_classes = [
    #     IsAuthenticated,
    #     IsAdminUser,
    # ]

    def post(self, request):

        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Customer Admin registered successfully",
                    "id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminTeamRegistrationAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    def post(self, request):

        serializer = AdminTeamRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Admin team member registered successfully",
                    "id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerAdminRegistrationAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]
    # Only authenticated users (admins) can access this API

    def post(self, request):

        serializer = CustomerAdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Customer Admin registered successfully",
                    "id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerTeamRegistrationAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsCustomerUser,
    ]

    def post(self, request):

        serializer = CustomerTeamRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Team memeber registered successfully",
                    "id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "id": user.id,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data["identifier"]
            # Here you can send an email or SMS to the user
            return Response(
                {"message": "Password reset link sent."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password updated successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialMediaLoginAPIView(APIView):
    def post(self, request):
        serializer = SocialMediaLoginSerializer(data=request.data)
        if serializer.is_valid():
            social_media_id = serializer.validated_data["social_media_id"]
            user = UserMaster.objects.filter(social_media_id=social_media_id).first()

            if user:
                # User exists, log them in and generate tokens
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "Login successful",
                        "id": user.id,
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # User does not exist, register them
                user_data = {
                    "social_media_id": social_media_id,
                    "password": "default_password",  # Use a more secure method in production
                    "user_type": 1,  # Set a default user type or handle this accordingly
                }
                registration_serializer = UserRegistrationSerializer(data=user_data)
                if registration_serializer.is_valid():
                    user = registration_serializer.save()
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "message": "User registered successfully",
                            "id": user.id,
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                        },
                        status=status.HTTP_201_CREATED,
                    )
                return Response(
                    registration_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
