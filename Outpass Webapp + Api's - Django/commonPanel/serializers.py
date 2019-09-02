from rest_framework import serializers
from .models import UserDetails
from django.contrib.auth.models import User

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('first_name', 'last_name', 'username', 'date_joined', 'last_login', 'email')

class UserDetailsSerializer(serializers.ModelSerializer):
    user=serializers.CharField(source="user.username")
    other_details=UserSerilizer(source="user")

    class Meta:
        model=UserDetails  # what module you are going to serialize
        fields= '__all__'
