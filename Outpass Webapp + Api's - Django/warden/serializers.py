from rest_framework import serializers
from .models import Warden, Notifications
from django.contrib.auth.models import User
from student.serializers import RegisteredCollegesSerializer
from commonPanel.serializers import UserDetailsSerializer

class WardenDetailsSerializer(serializers.ModelSerializer):
    warden=UserDetailsSerializer()
    college=RegisteredCollegesSerializer()

    class Meta:
        model=Warden
        fields='__all__'


class LimitedWardenDetailsSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(source="warden.user.first_name")
    last_name=serializers.CharField(source="warden.user.last_name")
    college=RegisteredCollegesSerializer()
    picture=serializers.CharField(source="warden.photo")
    phone=serializers.CharField(source="warden.phone")

    class Meta:
        model=Warden
        fields = ('er_no', 'first_name', 'last_name', 'college', 'year', 'semester', 'hostel', 'picture', 'phone')


class NotificationsSerializer(serializers.ModelSerializer):
    sender_f=serializers.CharField(source="sender.user.first_name")
    sender_l=serializers.CharField(source="sender.user.last_name")
    receiver=serializers.CharField(source="receiver.user.first_name")

    class Meta:
        model=Notifications
        fields=('sender_f', 'sender_l', 'receiver', 'date', 'text', 'id')
