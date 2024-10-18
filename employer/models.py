from django.db import models
from accounts.models import UserMaster
from shared_resources.models import Country
# Create your models here.
# Employer onboadring data models

class EmployerProfile(models.Model):
    employer_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=256, null=True)
    company_description = models.CharField(max_length=1000, null=True)
    website = models.CharField(max_length=256, null=True)
    business_registration_number = models.CharField(max_length=100, unique=True, null=True)
    tax_identification_number = models.CharField(max_length=256, unique=True, null=True)
    industry = models.CharField(max_length=256, null=True)
    size = models.CharField(max_length=100, null=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    headquarter_address = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("company_name", "country_id"),)

    def __str__(self):
        return self.company_name

class EmployerContacts(models.Model):
    contact_id = models.AutoField(primary_key=True)
    employer_id = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    email_address = models.CharField(max_length=255, null=True)
    job_title = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployerHRContacts(models.Model):
    hr_contact_id = models.AutoField(primary_key=True)
    employer_id = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    email_address = models.CharField(max_length=255, null=True)
    job_title = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployerDocuments(models.Model):
    document_id = models.AutoField(primary_key=True)
    employer_id = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    incorporation_document = models.CharField(max_length=255, blank=True, null=True)  # Store file path
    business_license = models.CharField(max_length=255, blank=True, null=True)  # Store file path
    insurance_document = models.CharField(max_length=255, blank=True, null=True)  # Store file path
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)