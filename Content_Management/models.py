from django.db import models
from datetime import datetime
from django.utils import timezone
from Admin_Management.models import CustomUser
# Create your models here.


# Recruiting position model
class Positions(models.Model):
    position_name = models.CharField(max_length=100, null=False)
    position_desc = models.CharField(max_length=300, null=True)
    position_state = models.CharField(max_length=10, default="Open")
    created_at    = models.DateTimeField(null=False, default=timezone.now)
    updated_at    = models.DateTimeField(null=False, default=timezone.now)


# Interview questions model
class Questions(models.Model):
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)
    question = models.CharField(max_length=500, null=False)
    question_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)


# Candidate profile model
class Candidate(models.Model):
    consultancy = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position = models.ForeignKey(Positions, null=True, default=None)
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


# Skill set added by HR
class MasterSkills(models.Model):
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)
    skill = models.CharField(max_length=50, null=False, default="Other Skill")
    description = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)


# candidate skillset model
class Skillset(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    master_skill = models.ForeignKey(MasterSkills, null=True, default=None)
    candidate_skill = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)


# The activity table to store the activities performed by consultancy or hr
class Activities(models.Model):
    consultancy = models.ForeignKey(CustomUser, null=True, default=None, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, null=True, default=None)
    position = models.ForeignKey(Positions, null=True, default=None)
    question = models.ForeignKey(Questions, null=True, default=None)
    activity = models.CharField(max_length=500, null=False)
    created_at = models.DateTimeField(null=False, default=timezone.now)