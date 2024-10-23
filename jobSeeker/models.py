from django.db import models
from accounts.models import UserMaster


class JobSeeker(models.Model):
    user_id = models.OneToOneField(UserMaster, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    profile_headline = models.CharField(max_length=255, null=True, blank=True)
    profile_photo = models.FileField(upload_to="profile_photos/", null=True, blank=True)

    def __str__(self):
        return self.full_name


class CareerPreferences(models.Model):
    job_seeker = models.OneToOneField(
        JobSeeker, related_name="career_preferences", on_delete=models.CASCADE
    )
    preferred_job_roles = models.JSONField(null=True, blank=True)
    preferred_cities = models.JSONField(null=True, blank=True)
    expected_annual_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    job_type = models.CharField(max_length=50, null=True, blank=True)
    employment_type = models.CharField(max_length=50, null=True, blank=True)
    preferred_shift = models.CharField(max_length=50, null=True, blank=True)


class BasicDetails(models.Model):
    job_seeker = models.OneToOneField(
        JobSeeker, related_name="basic_details", on_delete=models.CASCADE
    )
    work_status = models.CharField(max_length=50, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    current_city = models.CharField(max_length=100, null=True, blank=True)
    annual_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    salary_breakdown = models.CharField(max_length=50, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notice_period = models.CharField(max_length=50, null=True, blank=True)


class ResumeVideoProfile(models.Model):
    job_seeker = models.OneToOneField(
        JobSeeker, related_name="resume_video_profile", on_delete=models.CASCADE
    )
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)
    video_profile = models.FileField(upload_to="video_profiles/", null=True, blank=True)


class ProfessionalDetails(models.Model):
    job_seeker = models.OneToOneField(
        JobSeeker, related_name="professional_details", on_delete=models.CASCADE
    )
    current_industry = models.CharField(max_length=100, null=True, blank=True)
    current_department = models.CharField(max_length=100, null=True, blank=True)
    current_role_category = models.CharField(max_length=100, null=True, blank=True)
    current_job_role = models.CharField(max_length=100, null=True, blank=True)
    key_skills = models.JSONField(null=True, blank=True)


class Employment(models.Model):
    job_seeker = models.ForeignKey(
        JobSeeker, related_name="employments", on_delete=models.CASCADE
    )
    is_current_company = models.BooleanField(default=False, null=True, blank=True)
    employment_type = models.CharField(max_length=50, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    role_category = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    leaving_date = models.DateField(null=True, blank=True)
    job_profile = models.TextField(null=True, blank=True)


class Project(models.Model):
    job_seeker = models.ForeignKey(
        JobSeeker, related_name="projects", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    client = models.CharField(max_length=255, null=True, blank=True)
    project_status = models.CharField(max_length=50)
    worked_from = models.DateField(null=True, blank=True)
    worked_till = models.DateField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    project_location = models.CharField(max_length=100, null=True, blank=True)
    project_site = models.CharField(max_length=50, null=True, blank=True)
    nature_of_employment = models.CharField(max_length=50, null=True, blank=True)
    team_size = models.IntegerField(null=True, blank=True)
    role_in_project = models.CharField(max_length=100, null=True, blank=True)
    role_description = models.TextField(null=True, blank=True)
    skills_used = models.JSONField(null=True, blank=True)


class ITSkill(models.Model):
    job_seeker = models.ForeignKey(
        JobSeeker, related_name="it_skills", on_delete=models.CASCADE
    )
    skill_name = models.CharField(max_length=255, null=True, blank=True)
    software_version = models.CharField(max_length=100, null=True, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    last_used_year = models.IntegerField(null=True, blank=True)


class Education(models.Model):
    job_seeker = models.ForeignKey(
        JobSeeker, related_name="education", on_delete=models.CASCADE
    )
    education_option = models.CharField(max_length=100, null=True, blank=True)
    university_name = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    course_type = models.CharField(max_length=100, null=True, blank=True)
    course_duration_start = models.IntegerField(null=True, blank=True)  # Starting year
    course_duration_end = models.IntegerField(null=True, blank=True)  # Ending year
    grading_system = models.CharField(max_length=100, null=True, blank=True)


class Accomplishment(models.Model):
    job_seeker = models.ForeignKey(
        JobSeeker, related_name="accomplishments", on_delete=models.CASCADE
    )
    type = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    date_of_publish = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    patent_office = models.CharField(max_length=255, null=True, blank=True)
    patent_status = models.CharField(max_length=50, null=True, blank=True)
    application_number = models.CharField(max_length=100, null=True, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    completion_id = models.CharField(max_length=100, null=True, blank=True)
    validity = models.DateField(null=True, blank=True)


class PersonalDetail(models.Model):
    job_seeker = models.OneToOneField(JobSeeker, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, null=True, blank=True)
    marital_status = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    differently_abled = models.BooleanField(default=False, null=True, blank=True)
    disability_type = models.CharField(max_length=100, null=True, blank=True)
    assistance_required = models.BooleanField(default=False, null=True, blank=True)
    career_break = models.BooleanField(default=False, null=True, blank=True)
    break_reason = models.CharField(max_length=255, null=True, blank=True)
    break_duration = models.IntegerField(null=True, blank=True)  # Duration in months
    work_permit = models.BooleanField(default=False, null=True, blank=True)  # For USA
    permanent_address = models.TextField(null=True, blank=True)
    hometown = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)


class Language(models.Model):
    job_seeker = models.ForeignKey(
        JobSeeker, related_name="languages", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    proficiency = models.CharField(max_length=50, null=True, blank=True)
    comfortable_in = models.JSONField(null=True, blank=True)
