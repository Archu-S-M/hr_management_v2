from django.db import models

# getting user model

from django.contrib.auth.models import User, UserManager

# This is the extended user model for extra information

class CustomUser(User):
    consultancy_name = models.CharField(null=True, max_length=300)
    website = models.CharField(null=True, max_length=300)
    phone_no = models.CharField(null=True, max_length=20)

    objects = UserManager()
