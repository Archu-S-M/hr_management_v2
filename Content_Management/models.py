from django.db import models
from datetime import datetime
from django.utils import timezone
from Admin_Management.models import CustomUser
# Create your models here.

# Candidate profile model
class Candidate(models.Model):
    consultancy = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    candidate_name = models.CharField(max_length=100, null=False)
    candidate_age = models.IntegerField(null=False, default=22)
    candidate_experience = models.FloatField(null=True, default=0.0)
    preferred_location = models.CharField(max_length=200, null=True)
    current_ctc = models.FloatField(null=True, default=0.0)
    expected_ctc = models.FloatField(null=False, default=0.0)
    notice_period = models.CharField(null=True, max_length=10, default="IMMEDIATE")
    candidate_email = models.CharField(max_length=120, null=False)
    candidate_resume = models.CharField(max_length=100, null=True)
    candidate_interview = models.CharField(max_length=100, null=True)
    candidate_contact_no = models.CharField(max_length=15, null=False)
    candidate_interview_time = models.DateTimeField(null=True, default=timezone.now)
    candidate_status = models.CharField(max_length=10, null=True, default="VALID")
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)


# hr requirements model
class Requirements(models.Model):
    requirement_name = models.CharField(max_length=50, null=False)
    requirement_description = models.CharField(max_length=100, null=True)
    requirement_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)


# candidate skill set model
class Skillset(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    candidate_skill = models.CharField(max_length=50, null=True)
    requirement = models.ForeignKey(Requirements, null=True, default=None)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)



# Interview questions model
class Questions(models.Model):
    requirement = models.ForeignKey(Requirements, on_delete=models.CASCADE)
    question = models.CharField(max_length=500, null=False)
    question_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)


# The activity table to store the activities performed by consultancy or hr
class Activities(models.Model):
    consultancy = models.ForeignKey(CustomUser, null=True, default=None ,on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, null=True, default=None)
    requirement = models.ForeignKey(Requirements, null=True, default=None)
    question = models.ForeignKey(Questions, null=True, default=None)
    activity = models.CharField(max_length=500, null=False)
    created_at = models.DateTimeField(null=False, default=timezone.now)