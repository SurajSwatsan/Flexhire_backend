from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q  # Ensure Q is imported
from .models import UserMaster, RoleMaster
from django.contrib.auth import authenticate


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = ["role_id", "role_name", "parent"]

    def validate(self, attrs):
        # Ensure the role name is unique
        if RoleMaster.objects.filter(role_name=attrs["role_name"]).exists():
            raise serializers.ValidationError("Role name must be unique.")
        return attrs


class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = ["mobile_number", "email", "password"]

    def validate(self, attrs):
        # Ensure at least one identifier is provided
        if not (attrs.get("mobile_number") or attrs.get("email")):
            raise serializers.ValidationError(
                "You must provide either a mobile number or email."
            )

        # Ensure the Customer Admin role ID is correct
        customer_admin_role = RoleMaster.objects.get(role_name="Admin")
        attrs["user_type"] = customer_admin_role
        return attrs

    def create(self, validated_data):
        # Remove the password from validated_data for the user creation
        password = validated_data.pop("password")  # Extract password
        user = UserMaster(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user
        return user


class AdminTeamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = ["mobile_number", "email", "password", "user_type"]

    def validate(self, attrs):
        # Ensure at least one identifier is provided
        if not (attrs.get("mobile_number") or attrs.get("email")):
            raise serializers.ValidationError(
                "You must provide either a mobile number or email."
            )

        return attrs

    def create(self, validated_data):
        # Remove the password from validated_data for the user creation
        password = validated_data.pop("password")  # Extract password
        user = UserMaster(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user
        return user


class CustomerAdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = ["mobile_number", "email", "social_media_id", "password"]

    def validate(self, attrs):
        # Ensure at least one identifier is provided
        if not (attrs.get("mobile_number") or attrs.get("email")):
            raise serializers.ValidationError(
                "You must provide either a mobile number or email."
            )

        # Ensure the Customer Admin role ID is correct
        customer_admin_role = RoleMaster.objects.get(role_name="Employer")
        attrs["user_type"] = customer_admin_role
        return attrs

    def create(self, validated_data):
        # Remove the password from validated_data for the user creation
        password = validated_data.pop("password")  # Extract password
        user = UserMaster(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user
        return user


class CustomerTeamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = ["mobile_number", "email", "social_media_id", "password", "user_type"]

    def validate(self, attrs):
        # Ensure at least one identifier is provided
        if not (attrs.get("mobile_number") or attrs.get("email")):
            raise serializers.ValidationError(
                "You must provide either a mobile number or email."
            )

        return attrs

    def create(self, validated_data):
        # Remove the password from validated_data for the user creation
        password = validated_data.pop("password")  # Extract password
        user = UserMaster(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserMaster
        fields = ["mobile_number", "email", "social_media_id", "password"]

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
            and UserMaster.objects.filter(mobile_number=attrs["mobile_number"]).exists()
        ):
            raise serializers.ValidationError("Mobile number already in use.")
        if (
            attrs.get("email")
            and UserMaster.objects.filter(email=attrs["email"]).exists()
        ):
            raise serializers.ValidationError("Email already in use.")
        if (
            attrs.get("social_media_id")
            and UserMaster.objects.filter(
                social_media_id=attrs["social_media_id"]
            ).exists()
        ):
            raise serializers.ValidationError("Social media ID already in use.")
        # Ensure the Customer Admin role ID is correct
        customer_admin_role = RoleMaster.objects.get(role_name="Job Seeker")
        attrs["user_type"] = customer_admin_role
        return attrs

    def create(self, validated_data):
        # Remove the password from validated_data for the user creation
        password = validated_data.pop("password")  # Extract password
        user = UserMaster(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user
        return user

    # def create(self, validated_data):
    #     validated_data["user_password"] = make_password(validated_data.pop("password"))
    #     return super().create(validated_data)


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
        identifier = attrs.get("identifier")
        password = attrs.get("password")
        if "@" in identifier:
            # Assume identifier is an email
            user = authenticate(email=identifier, password=password)
        else:
            # Assume identifier is a mobile number
            try:
                user = UserMaster.objects.get(mobile_number=identifier)
                if not user.check_password(password):
                    user = None
            except UserMaster.DoesNotExist:
                user = None

        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        return user


class PasswordResetSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        if not UserMaster.objects.filter(
            Q(email=value) | Q(mobile_number=value) | Q(social_media_id=value)
        ).exists():
            raise serializers.ValidationError("Identifier not found.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_identifier(self, value):
        if not UserMaster.objects.filter(
            Q(email=value) | Q(mobile_number=value) | Q(social_media_id=value)
        ).exists():
            raise serializers.ValidationError("Identifier not found.")
        return value

    def save(self):
        identifier = self.validated_data["identifier"]
        new_password = self.validated_data["new_password"]
        user = UserMaster.objects.get(
            Q(email=identifier)
            | Q(mobile_number=identifier)
            | Q(social_media_id=identifier)
        )
        user.password_hash = make_password(new_password)
        user.save()
