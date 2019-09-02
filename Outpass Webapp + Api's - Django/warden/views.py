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
from commonPanel.models import Token
from student.models import Requests, outPass
from .serializers import WardenDetailsSerializer, LimitedWardenDetailsSerializer, NotificationsSerializer
import json
from student.serializers import outPassSerializer, StudentSerializer
from django.db.models import Count, IntegerField, CharField, Value
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .permissions import WardenAccessPermissions, WardenAccessPermissionsWithoutVerification

@login_required(login_url="/user/login")
def mainPage(request):
    if(UserDetails.objects.get(user=request.user).type=="S"):
        return HttpResponseRedirect('/student/mainPage')

    elif(UserDetails.objects.get(user=request.user).type=="W"):
        token=Token.objects.get(user=request.user)
        print(token.access_token)
        return render(request, "warden/mainPage.html", {"access_token":token.access_token , "refresh_token":token.refresh_token})

@api_view(['POST'])
@permission_classes((IsAuthenticated, WardenAccessPermissionsWithoutVerification, ))
def saveWardenDetails(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    try:
        #print(params)
        obj,notif=Warden.objects.get_or_create(warden=UserDetails.objects.get(user=request.user))
        obj.er_no=params['er_no']
        obj.year=params['year']
        obj.semester=params['sem']
        obj.college=RegisteredColleges.objects.get(shortHand=params['college'])
        obj.hostel=params['hostel']
        obj.signature=params['signature']
        obj.id_card=params['id_pic']
        obj.save()
        generateRequest(UserDetails.objects.get(user=request.user), obj.college)

        return JsonResponse({"message": "Success", "status":"200"})
    except Exception as e:
        return JsonResponse({"message": "Error", "status":"404"})


def generateRequest(user, college):
    senderRequests=Requests.objects.filter(sender=user)
    if(senderRequests.count()>0):
        sender=Requests.objects.get(sender=user)
        sender.college=college
        sender.save()
        print("Ok Saved Successfully")
    else:
        obj,notif=Requests.objects.get_or_create(sender=user, college=college, typeOfRequest="W")
        if(notif):
            obj.save()
            print("Ok Saved Successfully")
        else:
            print("Error In Saving Request")

@api_view(['GET'])
@permission_classes((IsAuthenticated, WardenAccessPermissionsWithoutVerification, ))
def wardenDetails(request, format=None):
    student=Warden.objects.filter(warden=UserDetails.objects.get(user=request.user))
    serializer=WardenDetailsSerializer(student, many=True)

    return JsonResponse({"message": "Success","warden_details":json.dumps(serializer.data), "status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def pendingOutpassRequests(request, format=None):
    pending_outpassRequests=outPass.objects.filter(student__id__in=Warden.objects.get(warden=UserDetails.objects.get(user=request.user)).student.all().values('student__id'), saved=False, approved_by_warden=False).order_by('-isEmergency')
    print(pending_outpassRequests)
    outpasses=outPassSerializer(pending_outpassRequests, many=True)
    return JsonResponse({"message": "Success","pending_outpasses":json.dumps(outpasses.data), "status":"200"})


@api_view(['PUT'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def acceptOutpass(request, format=None):
    params=request.data
    if(outPass.objects.filter(outpassId=params['id']).count()>0):
        outpass=outPass.objects.get(outpassId=params['id'])
        outpass.approved_by_warden=True
        outpass.save()
        print("ok")
        generateNotification(outpass, request, "O")
        return JsonResponse({"message": "Accepted", "status":"200"})
    else:
        return JsonResponse({"message": "Not Found", "status":"404"})

@api_view(['GET'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def acceptedOutpassRequests(request, format=None):
    accepted_outpassRequests=outPass.objects.filter(student__id__in=Warden.objects.get(warden=UserDetails.objects.get(user=request.user)).student.all().values('student__id'), saved=False, approved_by_warden=True).order_by('-isEmergency')
    print(accepted_outpassRequests)
    outpasses=outPassSerializer(accepted_outpassRequests, many=True)
    return JsonResponse({"message": "Success","pending_outpasses":json.dumps(outpasses.data), "status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def outpassOverview(request, format=None):

    obj=outPass.objects.filter(student__id__in=Warden.objects.get(warden=UserDetails.objects.get(user=request.user)).student.all().values('student__id')).values(
        'student__id', 'student__user__username', 'student__phone', 'student__photo', 'student__user__first_name', 'student__user__last_name'
    ).annotate(
        approved=Count('approved_by_warden', filter=Q(approved_by_warden=True)),
        pending=Count('approved_by_warden', filter=Q(saved=False) & Q(approved_by_warden=False)),
    )

    serialized_q = json.dumps(list(obj), cls=DjangoJSONEncoder)
    print(serialized_q)

    return JsonResponse({"message": "Success","overview":serialized_q, "status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def makeWardenRequests(request, format=None):
    makeWardenRequests=Warden.objects.filter(isVerified=False, college=Warden.objects.get(warden=UserDetails.objects.get(user=request.user)).college)
    serializedmakeWardenRequests=LimitedWardenDetailsSerializer(makeWardenRequests, many=True)

    return JsonResponse({"message": "Success","warden_requests":json.dumps(serializedmakeWardenRequests.data), "status":"200"})


@api_view(['PUT'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def acceptWardenRequest(request, format=None):
    makeWarden=Warden.objects.get(er_no=request.data['id'])
    if(makeWarden.isVerified==True):
        return JsonResponse({"message": "Already A Verified Warden", "status":"404"})
    else:
        makeWarden.isVerified=True
        makeWarden.save()
        return JsonResponse({"message": "Accepted", "status":"200"})

@api_view(['DELETE'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def deleteFakeWarden(request, format=None):
    try:
        User.objects.get(current=UserDetails.objects.get(warden_name__er_no=request.data['id'])).delete()
        return JsonResponse({"mes":"Success", "status":"200"})
    except Exception as e:
        print(e)
        return JsonResponse({"mes":"Error", "status":"404"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def generateOutpass(request, format=None):
    params=request.GET
    outpass=outPass.objects.get(outpassId=params.get('id'))

    student=outpass.student
    student1=Student.objects.get(student__id=student.id)
    college=student1.college
    warden=Warden.objects.get(student__exact=student1)

    data={
            "college_logo":college.logo.name,
            "college_fullName":college.fullName,
            "college_location":college.location,
            "college_pincode":college.pincode,
            "college_country":college.country,
            "student_fullName":student.user.first_name+" "+student.user.last_name,
            "student_branch":student1.branch,
            "student_email":student.user.email,
            "student_bed":student1.bed_no,
            "student_er_no":student1.er_no,
            "student_year":student1.year,
            "student_semester":student1.semester,
            "student_room":student1.room_no,
            "student_hostel":student1.hostel,
            "student_phone":str(student.phone),
            "student_parent_name":student1.parent,
            "student_parent_phone":str(student1.parent_contact),
            "days":outpass.no_of_days,
            "from":str(outpass.fromDate),
            "to":str(outpass.toDate),
            "purposeOfLeave":outpass.purposeOfLeave,
            "addressWhileLeave":outpass.addressWhileLeave,
            "student_signature":student1.signature,
            "warden_fullName":warden.warden.user.first_name+" "+warden.warden.user.last_name,
            "warden_signature":warden.signature
    }

    return JsonResponse({"message":"Success", "data":json.dumps(data), "status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, WardenAccessPermissions,))
def allpendingNotifications(request, format=None):
    makeWardenRequests=Warden.objects.filter(isVerified=False, college=Warden.objects.get(warden=UserDetails.objects.get(user=request.user)).college)
    serializedmakeWardenRequests=LimitedWardenDetailsSerializer(makeWardenRequests, many=True)
    pending_outpassRequests=outPass.objects.filter(student__id__in=Warden.objects.get(warden=UserDetails.objects.get(user=request.user)).student.all().values('student__id'), saved=False, approved_by_warden=False)
    outpasses=outPassSerializer(pending_outpassRequests, many=True)
    return JsonResponse({"message": "Success","warden_requests":json.dumps(serializedmakeWardenRequests.data), "pending_outpasses":json.dumps(outpasses.data),"total":makeWardenRequests.count()+pending_outpassRequests.count() ,"status":"200"})


# Generate Notifications
def generateNotification(outpass, request, type):
    outpass1=Notifications.objects.get(outpass=outpass)
    obj, notif=Notifications.objects.get_or_create(sender=outpass1.receiver, receiver=outpass1.sender, type=type, outpass=outpass ,text="Hey I Accept Your Request For Your OutpassId {}".format(outpass.outpassId))
    if(notif):
        obj.save()

        becomeWardenRequests1
