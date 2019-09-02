from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField
from commonPanel.models import UserDetails
from jsignature.forms import JSignatureField
from phonenumber_field.modelfields import PhoneNumberField

class RegisteredColleges(models.Model):
    collegeId=models.AutoField(primary_key=True)
    fullName=models.CharField(max_length=200)
    shortHand=models.CharField(max_length=100)
    location=models.TextField()
    pincode=models.CharField(max_length=100, null=True, blank=True)
    country=models.CharField(max_length=100, null=True, blank=True)
    email=models.EmailField()
    website_url=models.URLField(max_length=100)
    contact_no= PhoneNumberField(blank=True, help_text='Contact phone number')
    logo=models.FileField(upload_to='College Logos', null=True, blank=True)

    def __str__(self):
        return self.fullName

class outPass(models.Model):
    outpassId=models.AutoField(primary_key=True)
    student=models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    createdDate=models.DateTimeField(auto_now=True)
    title=models.CharField(max_length=100, null=True, blank=True)
    no_of_days=models.PositiveIntegerField(null=True, blank=True)
    whatsappImg=models.FileField(upload_to='Whatsapp ScreenShots', null=True, blank=True)
    fromDate=models.DateField(null=True, blank=True)
    toDate=models.DateField(null=True, blank=True)
    purposeOfLeave=models.TextField(null=True, blank=True)
    addressWhileLeave=models.TextField(null=True, blank=True)
    approved_by_warden=models.BooleanField(default=False)
    generated_pdf=models.FileField(upload_to="Generated Pdf's", null=True, blank=True)
    isEmergency=models.BooleanField(default=False)
    saved=models.BooleanField(default=False)
    uniqueHash=models.CharField(max_length=500, null=True, blank=True)
    mark_as_read=models.BooleanField(default=False)

    def __str__(self):
        return self.student.user.username + " is saved - " + str(self.saved) + "; is approved_by_warden - " + str(self.approved_by_warden)


class Student(models.Model):
    student=models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    er_no=models.CharField(max_length=7, null=True, blank=True)
    year=models.PositiveIntegerField(null=True, blank=True)
    semester=models.PositiveIntegerField(null=True, blank=True)
    branch=models.CharField(max_length=50, null=True, blank=True)
    college=models.ForeignKey(RegisteredColleges, on_delete=models.CASCADE, null=True, blank=True)
    hostel=models.CharField(max_length=50, null=True, blank=True)
    room_no=models.CharField(max_length=50, null=True, blank=True)
    bed_no=models.PositiveIntegerField(null=True, blank=True)
    parent=models.CharField(max_length=100, null=True, blank=True)
    parent_contact= PhoneNumberField(null=True, blank=True, help_text="Parent's Contact phone number")
    signature=models.TextField(null=True, blank=True)
    isVerified=models.BooleanField(default=False)

    def __str__(self):
        return self.student.user.username

class Requests(models.Model):
    sender=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="sender")
    date=models.DateField(auto_now=True)
    typeOfRequest=models.CharField(max_length=50)
    college=models.ForeignKey(RegisteredColleges, on_delete=models.CASCADE, null=True, blank=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return "From:- "+self.sender.user.username+" for:- "+self.college.fullName
