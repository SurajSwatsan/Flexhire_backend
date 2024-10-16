from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q  # Ensure Q is imported
from .models import User, RoleMaster


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = ["id", "name", "parent"]

    def validate(self, attrs):
        # Ensure the role name is unique
        if RoleMaster.objects.filter(name=attrs["name"]).exists():
            raise serializers.ValidationError("Role name must be unique.")
        return attrs


class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["mobile_number", "email", "social_media_id", "password_hash"]

    def validate(self, attrs):
        # Ensure at least one identifier is provided
        if not (attrs.get("mobile_number") or attrs.get("email")):
            raise serializers.ValidationError(
                "You must provide either a mobile number or email."
            )

        # Ensure the Customer Admin role ID is correct
        customer_admin_role = RoleMaster.objects.get(name="Admin")
        attrs["role_id"] = customer_admin_role.id
        return attrs


class CustomerAdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["mobile_number", "email", "social_media_id", "password_hash"]

    def validate(self, attrs):
        # Ensure at least one identifier is provided
        if not (attrs.get("mobile_number") or attrs.get("email")):
            raise serializers.ValidationError(
                "You must provide either a mobile number or email."
            )

        # Ensure the Customer Admin role ID is correct
        customer_admin_role = RoleMaster.objects.get(name="Customer Admin")
        attrs["role_id"] = customer_admin_role.id
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.PrimaryKeyRelatedField(queryset=RoleMaster.objects.all())

    class Meta:
        model = User
        fields = ["mobile_number", "email", "social_media_id", "password", "user_type"]

    def validate(self, attrs):
        if not (
            attrs.get("mobile_number")
            or attrs.get("email")
            or attrs.get("social_media_id")
        ):
            raise serializers.ValidationError(
                "At least one of mobile number, email, or social media ID must be provided."
            )

        if (
            attrs.get("mobile_number")
            and User.objects.filter(mobile_number=attrs["mobile_number"]).exists()
        ):
            raise serializers.ValidationError("Mobile number already in use.")
        if attrs.get("email") and User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Email already in use.")
        if (
            attrs.get("social_media_id")
            and User.objects.filter(social_media_id=attrs["social_media_id"]).exists()
        ):
            raise serializers.ValidationError("Social media ID already in use.")

        return attrs

    def create(self, validated_data):
        validated_data["password_hash"] = make_password(validated_data.pop("password"))
        return super().create(validated_data)


class SocialMediaLoginSerializer(serializers.Serializer):
    social_media_id = serializers.CharField()

    def validate_social_media_id(self, value):
        if not value:
            raise serializers.ValidationError("Social media ID is required.")
        return value


class UserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(
            Q(email=attrs["identifier"])
            | Q(mobile_number=attrs["identifier"])
            | Q(social_media_id=attrs["identifier"])
        ).first()

        if user and check_password(attrs["password"], user.password_hash):
            return user
        raise serializers.ValidationError("Invalid credentials.")


class PasswordResetSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        if not User.objects.filter(
            Q(email=value) | Q(mobile_number=value) | Q(social_media_id=value)
        ).exists():
            raise serializers.ValidationError("Identifier not found.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_identifier(self, value):
        if not User.objects.filter(
            Q(email=value) | Q(mobile_number=value) | Q(social_media_id=value)
        ).exists():
            raise serializers.ValidationError("Identifier not found.")
        return value

    def save(self):
        identifier = self.validated_data["identifier"]
        new_password = self.validated_data["new_password"]
        user = User.objects.get(
            Q(email=identifier)
            | Q(mobile_number=identifier)
            | Q(social_media_id=identifier)
        )
        user.password_hash = make_password(new_password)
        user.save()
