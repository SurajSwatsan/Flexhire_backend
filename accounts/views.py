from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .models import User, RoleMaster
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    PasswordResetSerializer,
    SetNewPasswordSerializer,
    SocialMediaLoginSerializer,
    RoleSerializer,
    CustomerAdminRegistrationSerializer,
)
from django.http import Http404
from .permissions import IsAdminUser  # Import the custom permission
from rest_framework.permissions import IsAuthenticated


class RoleListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        roles = RoleMaster.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            role = serializer.save()
            return Response(
                {"message": "Role created successfully", "role_id": role.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return RoleMaster.objects.get(pk=pk)
        except RoleMaster.DoesNotExist:
            raise Http404("Role not found.")

    def get(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Role updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response(
            {"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class CustomerAdminRegistrationAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]  # Only authenticated users (admins) can access this API

    def post(self, request):
        # Check if the requesting user is an admin
        if request.user.user_type.name != "Admin":
            return Response(
                {"detail": "Only admins can register a Customer Admin."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CustomerAdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Customer Admin registered successfully",
                    "user_id": user.user_id,
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
                {"message": "User registered successfully", "user_id": user.user_id},
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
                    "user_id": user.user_id,
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
            user = User.objects.filter(social_media_id=social_media_id).first()

            if user:
                # User exists, log them in and generate tokens
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "Login successful",
                        "user_id": user.user_id,
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
                            "user_id": user.user_id,
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                        },
                        status=status.HTTP_201_CREATED,
                    )
                return Response(
                    registration_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
