from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField
from phonenumber_field.modelfields import PhoneNumberField

class UserDetails(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="current")
    gender=models.CharField(max_length=100)
    phone= PhoneNumberField(null=True, blank=True, help_text='Contact phone number')
    phone1= PhoneNumberField(null=True, blank=True, help_text='Contact phone number')
    country=models.CharField(max_length=100, default=None)
    city=models.CharField(max_length=100, default=None)
    state=models.CharField(max_length=100, default=None)
    type=models.CharField(max_length=100)
    dob=models.DateField()
    photo=models.FileField(upload_to='profile_pictures', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Token(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    access_token=models.CharField(max_length=500)
    refresh_token=models.CharField(max_length=500)

    def __str__(self):
        return self.user.username
