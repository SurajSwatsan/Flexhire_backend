from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from shared_resources.models import Country


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class RoleMaster(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sub_roles",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role_name


class UserMaster(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    social_media_id = models.CharField(max_length=255, unique=True, null=True)
    user_password = models.CharField(max_length=255, null=True)
    user_type = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="parent_user",
    )
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email or self.mobile_number or self.social_media_id
