from django.db import models

class RoleMaster(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_roles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    social_media_id = models.CharField(max_length=255, unique=True, null=True)
    password_hash = models.CharField(max_length=255)
    user_type = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email or self.mobile_number or self.social_media_id
