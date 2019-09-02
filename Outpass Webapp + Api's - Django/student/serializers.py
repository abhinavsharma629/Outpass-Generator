from rest_framework import serializers
from .models import RegisteredColleges, Requests, outPass, Student
from django.contrib.auth.models import User
from commonPanel.serializers import UserDetailsSerializer

class RegisteredCollegesSerializer(serializers.ModelSerializer):

    class Meta:
        model=RegisteredColleges  # what module you are going to serialize
        fields= '__all__'

class RequestsSerializer(serializers.ModelSerializer):
    sender=serializers.CharField(source="sender.user.username")
    receiver=serializers.CharField(source="receiver.user.username")

    class Meta:
        model=Requests  # what module you are going to serialize
        fields= ('sender','receiver','date','typeOfRequest','status')

class StudentSerializer(serializers.ModelSerializer):
    student=UserDetailsSerializer()
    # parent = serializers.SerializerMethodField()
    college=RegisteredCollegesSerializer()

    class Meta:
        model=Student  # what module you are going to serialize
        fields= '__all__'

    # def get_parent(self, obj):
    #     if(obj.parent):
    #         return obj.parent.parent.user.username
    #     else:
    #         return None

class outPassSerializer(serializers.ModelSerializer):
    student=UserDetailsSerializer()

    class Meta:
        model=outPass  # what module you are going to serialize
        exclude = ('uniqueHash',)
