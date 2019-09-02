from django.shortcuts import render,redirect
from django.template import loader
from django import forms
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import *
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.utils.dateparse import parse_date
import requests
from django.contrib.auth.decorators import login_required
from student.models import Student
from phonenumber_field.phonenumber import PhoneNumber
from warden.models import Warden
import requests

@api_view(['POST'])
@permission_classes((AllowAny, ))
def createUser(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    print(params)
    obj, notif=User.objects.get_or_create(username=params['username'], email=params['email'])
    obj.set_password(params['pass'])
    print(notif)
    if(notif):
        obj.save()
        obj.first_name=params['fname']
        obj.last_name=params['lname']
        obj.save()
        date = parse_date(params['dob'])
        phone=PhoneNumber.from_string(phone_number=params['phone'], region='IN').as_e164
        try:
            phone1=PhoneNumber.from_string(phone_number="+91"+params['phone1'], region='IN').as_e164
        except Exception as e:
            phone1=params['phone1']
        obj1, notif1=UserDetails.objects.get_or_create(user=User.objects.get(username=params['username']), gender=params['gender'], phone=phone, phone1=phone1, country=params['country'], city=params['city'], state=params['state'], dob=date, type=params['type'], photo=params['file'])
        if(notif1):
            obj1.save()
            if(params['type']=="S"):
                obj2, notif2=Student.objects.get_or_create(student=UserDetails.objects.get(user__username=params['username']))
                print(notif2)
                if(notif2):
                    print("ok",notif2)
                    obj2.save()
            elif(params['type']=="W"):
                obj2, notif2=Warden.objects.get_or_create(warden=UserDetails.objects.get(user__username=params['username']))
                print(notif2)
                if(notif2):
                    print("ok",notif2)
                    obj2.save()
            user=authenticate(username=params['username'], password=params['pass'])
            if(user is not None):
                login(request, user)

                url = "http://127.0.0.1:8000/user/api/token/"

                payload = {
                "username":params['username'],
                "password":params['pass']
                }
                headers = {
                    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                    'Content-Type': "application/x-www-form-urlencoded",
                    'cache-control': "no-cache"
                    }

                response = requests.request("POST", url, data=payload, headers=headers).json()
                print(response)
                obj3, notif3=Token.objects.get_or_create(user=user , access_token=response['access'], refresh_token=response['refresh'])
                if(notif3):
                    print("ok token saved")
                    obj3.save()
                    return JsonResponse({"message":"Success", "status":"200"})
                else:
                    return JsonResponse({"message":"Error", "status":"404"})
            else:
                return JsonResponse({"message":"Error", "status":"404"})
        else:
            return JsonResponse({"message":"Error", "status":"500"})
    else:
        return JsonResponse({"message":"Error", "status":"404"})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def validateUser(request, format=None):
    params=request.data
    print(params)
    user=authenticate(username=params['username'], password=params['pass'])
    print(user)
    if(user is not None):
        login(request, user)

        url = "http://127.0.0.1:8000/user/api/token/"

        payload = {
        "username":params['username'],
        "password":params['pass']
        }
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
            }

        response = requests.request("POST", url, data=payload, headers=headers).json()
        obj3=Token.objects.get(user=user)
        obj3.access_token=response['access']
        obj3.refresh_token=response['refresh']
        obj3.save()

        return JsonResponse({"message": "Success", "status":"200"})
    else:
        return JsonResponse({"message": "Success", "status":"404"})


@login_required(login_url='/user/login')
def mainPage(request):
    obj=UserDetails.objects.get(user=request.user).type
    print(obj)

    if(obj=="S"):
        return HttpResponseRedirect('/student/mainPage')
    else:
        return HttpResponseRedirect('/warden/mainPage')

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def tokenDetails(request, format=None):
    try:
        obj=Token.objects.get(user=request.user)
        return JsonResponse({"message":"Success", 'access_token':obj.access_token, "refresh_token":obj.refresh_token, "status":"200"})
    except:
        return JsonResponse({"message":"Error", "status":"404"})
