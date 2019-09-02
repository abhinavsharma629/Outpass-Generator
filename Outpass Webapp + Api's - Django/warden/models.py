from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField
from commonPanel.models import UserDetails
from jsignature.forms import JSignatureField
from student.models import RegisteredColleges, Student, outPass

class Warden(models.Model):
    warden=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="warden_name")
    er_no=models.CharField(max_length=50, null=True, blank=True)
    college=models.ForeignKey(RegisteredColleges, on_delete=models.CASCADE, null=True, blank=True)
    student=models.ManyToManyField(Student, blank=True)
    year=models.CharField(max_length=50, null=True, blank=True)
    semester=models.CharField(max_length=50, null=True, blank=True)
    hostel=models.CharField(max_length=50, blank=True, null=True)
    #signature = JSignatureField()
    signature=models.TextField(null=True, blank=True)
    id_card=models.FileField(upload_to='Warden Id', null=True, blank=True)
    isVerified=models.BooleanField(default=False)

    def __str__(self):
        return self.warden.user.username

class Notifications(models.Model):
    sender=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="sent_by")
    receiver=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="received_by")
    type=models.CharField(max_length=50, null=True, blank=True)
    outpass=models.ForeignKey(outPass, on_delete=models.CASCADE, null=True, blank=True)
    text=models.TextField(null=True, blank=True)
    college=models.ForeignKey(RegisteredColleges, on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateField(auto_now=True)
    isRead=models.BooleanField(default=False)
