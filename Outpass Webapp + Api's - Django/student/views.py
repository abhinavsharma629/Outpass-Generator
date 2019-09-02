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
import json
from .serializers import RegisteredCollegesSerializer, StudentSerializer, outPassSerializer, RequestsSerializer
from jsignature.utils import draw_signature
from commonPanel.models import Token
from phonenumber_field.phonenumber import PhoneNumber
from warden.models import Warden, Notifications
from warden.serializers import WardenDetailsSerializer, LimitedWardenDetailsSerializer, NotificationsSerializer
from django.utils.dateparse import parse_date
from warden.permissions import StudentAccessPermissions

# For 2 way encryption
import cryptography
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


password_provided = "abhi629@@" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once


@login_required(login_url="/user/login")
def mainPage(request):
    if(UserDetails.objects.get(user=request.user).type=="W"):
        return HttpResponseRedirect('/warden/mainPage')

    elif(UserDetails.objects.get(user=request.user).type=="S"):
        token=Token.objects.get(user=request.user)
        print(token.access_token)
        return render(request, "student/mainPage.html", {"access_token":token.access_token , "refresh_token":token.refresh_token})

@api_view(['POST'])
@permission_classes((IsAuthenticated, StudentAccessPermissions, ))
def saveStudentDetails(request, format=None):
    params=request.data
    try:
        #print(params)
        obj=Student.objects.get(student=UserDetails.objects.get(user=request.user))
        obj.er_no=params['er_no']
        obj.college=RegisteredColleges.objects.get(shortHand=params['college'])
        obj.year=params['year']
        obj.semester=params['sem']
        obj.branch=params['branch']
        obj.hostel=params['hostel']
        obj.parent=params['parent']
        obj.parent_contact=PhoneNumber.from_string(phone_number=params['parent_contact'], region='IN').as_e164
        obj.room_no=params['room_no']
        obj.bed_no=params['bed_no']
        obj.signature=params['signature']
        obj.save()
        print(obj.id)
        print(len(params['warden']))
        if(len(params['warden'])>0):
            print("inside year")
            #print(Warden.objects.get(student__id__in=[obj.id]).er_no, params['warden'])
            if(Warden.objects.filter(student__id__in=[obj.id]).count()>0):
                if(params['warden']!=Warden.objects.get(student__exact=obj).er_no):
                    print("inside final")
                    Warden.objects.get(student__exact=obj).student.remove(obj)
                    outPass.objects.filter(student=UserDetails.objects.get(user=request.user), saved=False).delete()

        if('year' in params and len(params['warden'])>0):
            warden=Warden.objects.get(er_no=params['warden'])
            if(warden.year==params['year']):
                print("equal")
                warden.student.add(obj)
                warden.save()
            else:
                return JsonResponse({"message": "Warden Is From Another Year", "status":"404"})

        elif(len(params['warden'])==0):
            print("inside 0")
            if(Warden.objects.filter(student__exact=obj.id).count()>0):
                if(params['warden']!=Warden.objects.get(student__exact=obj).er_no):
                    print("inside final")
                    Warden.objects.get(student__exact=obj).student.remove(obj)
                    outPass.objects.filter(student=UserDetails.objects.get(user=request.user), saved=False).delete()



        return JsonResponse({"message": "Success", "status":"200"})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error", "status":"500"})

@api_view(['GET'])
@permission_classes((AllowAny, ))
def registeredColleges(request, format=None):
    obj=RegisteredColleges.objects.all()
    serializers=RegisteredCollegesSerializer(obj,many=True)
    return JsonResponse({"message": "Success", "college_list":json.dumps(serializers.data) ,"status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def pendingRequests(request, format=None):
    typeOfRequest=request.GET.get("typeOfRequest")
    sentRequests=Requests.objects.filter(sender=UserDetails.objects.get(user=request.user), status="False")
    sentRequestsSerializer=RequestsSerializer(sentRequests, many=True)
    return JsonResponse({"message": "Success","sent_requests":json.dumps(sentRequestsSerializer.data), "status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def studentDetails(request, format=None):
    student=Student.objects.filter(student=UserDetails.objects.get(user=request.user))
    serializer=StudentSerializer(student, many=True)

    warden=Warden.objects.filter(student__id__in=[Student.objects.get(student=UserDetails.objects.get(user=request.user)).id])
    serializer1=LimitedWardenDetailsSerializer(warden, many=True)
    #print(json.dumps(serializer1.data, indent=4))

    return JsonResponse({"message": "Success","student_details":json.dumps(serializer.data),"warden":json.dumps(serializer1.data), "status":"200"})

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def savedOutpass(request, format=None):
    student=outPass.objects.filter(student=UserDetails.objects.get(user=request.user), saved=True).order_by('fromDate')
    serializer=outPassSerializer(student, many=True)

    return JsonResponse({"message": "Success","saved_outpasses":json.dumps(serializer.data), "status":"200"})

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def outpassHistory(request, format=None):
    student=outPass.objects.filter(student=UserDetails.objects.get(user=request.user), saved=False).order_by('fromDate')
    serializer=outPassSerializer(student, many=True)

    return JsonResponse({"message": "Success","approved_outpasses":json.dumps(serializer.data), "status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def isVerified(request, format=None):
    # student=Student.objects.filter(student=UserDetails.objects.get(user=request.user), isVerified=True).count()
    # print(student)
    # if(student==0):
    #     return JsonResponse({"message": "Not Verified", "status":"200"})
    # else:
    #     return JsonResponse({"message": "Verified", "status":"200"})
    if(Warden.objects.filter(student__exact=Student.objects.get(student=UserDetails.objects.get(user=request.user))).count()==0):
        return JsonResponse({"message": "Not Verified", "status":"200"})
    else:
        return JsonResponse({"message": "Verified", "status":"200"})



@api_view(['GET'])
@permission_classes((AllowAny, ))
def collegeWardens(request, format=None):
    print(request.GET.get("college"))
    warden=Warden.objects.filter(college__shortHand=request.GET.get("college"), isVerified=True)
    print(warden)
    warden_serializer=LimitedWardenDetailsSerializer(warden, many=True)

    return JsonResponse({"message": "Success", "warden_list":json.dumps(warden_serializer.data) , "status":"200"})

@api_view(['POST'])
@permission_classes((IsAuthenticated, StudentAccessPermissions,))
def saveOutpass(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    print(params)
    try:
        if('whtsImg' in params):
            outpass, notif=outPass.objects.get_or_create(student=UserDetails.objects.get(user=request.user), no_of_days=(int)(params['nod']), whatsappImg=params['whtsImg'], fromDate=parse_date(params['from']), toDate=parse_date(params['to']), purposeOfLeave=params['reason'], addressWhileLeave=params['add'], saved=True)
        else:
            outpass, notif=outPass.objects.get_or_create(student=UserDetails.objects.get(user=request.user),  no_of_days=(int)(params['nod']), fromDate=parse_date(params['from']), toDate=parse_date(params['to']), purposeOfLeave=params['reason'], addressWhileLeave=params['add'], saved=True)
        if(notif):
            outpass.save()
            return JsonResponse({"message": "Success", "status":"201"})
        else:
            return JsonResponse({"message": "Error", "status":"500"})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error", "status":"500"})

@api_view(['POST'])
@permission_classes((IsAuthenticated, StudentAccessPermissions, ))
def sendOutpass(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    print(params)

    if(outPass.objects.filter(student=UserDetails.objects.get(user=request.user), saved=False, approved_by_warden=False).count()>0):
        return JsonResponse({"message": "Error", "status":"404"})
    else:
        try:
            print(params['emergency'], type(params['emergency']))
            if(params['emergency']=="true"):
                emergency=True
            else:
                emergency=False
            if('whtsImg' in params):
                outpass, notif=outPass.objects.get_or_create(student=UserDetails.objects.get(user=request.user), no_of_days=(int)(params['nod']), whatsappImg=params['whtsImg'], fromDate=parse_date(params['from']), toDate=parse_date(params['to']), purposeOfLeave=params['reason'], addressWhileLeave=params['add'], isEmergency=emergency, saved=False, approved_by_warden=False)
            else:
                outpass, notif=outPass.objects.get_or_create(student=UserDetails.objects.get(user=request.user), no_of_days=(int)(params['nod']), fromDate=parse_date(params['from']), toDate=parse_date(params['to']), purposeOfLeave=params['reason'], addressWhileLeave=params['add'], isEmergency=emergency, saved=False, approved_by_warden=False)
            if(notif):
                outpass.save()
                generateNotification(outpass,request, "SO")
                return JsonResponse({"message": "Success", "status":"201"})
            else:
                return JsonResponse({"message": "Error", "status":"500"})
        except Exception as e:
            print(e)
        return JsonResponse({"message": "Error", "status":"500"})


# Generate Notifications
def generateNotification(outpass, request, type):
    sender=UserDetails.objects.get(user=request.user)
    if(type=="SO"):
        receiver=Warden.objects.get(student__exact=Student.objects.get(student=sender))
        obj, notif=Notifications.objects.get_or_create(sender=sender, receiver=receiver.warden, type=type, outpass=outpass ,text="Hey I Request You To Verify My Outpass With OutpassId {}".format(outpass.outpassId))
        if(notif):
            obj.save()


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
def removePendingOutpass(request, format=None):
    try:
        if(outPass.objects.filter(outpassId=request.data['id']).count()>0):
            outPass.objects.get(outpassId=request.data['id']).delete()
            return JsonResponse({"message": "Success", "status":"200"})
        else:
            return JsonResponse({"message": "Error", "status":"404"})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error", "status":"500"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def outpassDetails(request, format=None):
    try:
        if(outPass.objects.filter(outpassId=request.GET.get('id')).count()>0):
            outPass1=outPass.objects.filter(outpassId=request.GET.get('id'))
            serializer=outPassSerializer(outPass1, many=True)
            return JsonResponse({"message": "Success","details":json.dumps(serializer.data), "status":"200"})
        else:
            return JsonResponse({"message": "Error", "status":"404"})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error", "status":"500"})



@api_view(['PUT'])
@permission_classes((IsAuthenticated, StudentAccessPermissions, ))
def editOutpass(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    print(params)
    outPass1=outPass.objects.get(outpassId=params['id'])
    if(outPass1.saved==True):
        outPass1.no_of_days=(int)(params['nod'])
        outPass1.fromDate=parse_date(params['from'])
        outPass1.toDate=parse_date(params['to'])
        outPass1.purposeOfLeave=params['reason']
        outPass1.addressWhileLeave=params['add']
        if('whtsImg' in params):
            outPass1.whatsappImg=params['whtsImg']
        outPass1.save()
        return JsonResponse({"message":"Success", "status":"200"})
    else:
        return JsonResponse({"message":"Not Found", "status":"404"})


@api_view(['PUT'])
@permission_classes((IsAuthenticated, StudentAccessPermissions, ))
def sendSavedOutpass(request, format=None):
    params=request.data

    if(outPass.objects.filter(student=UserDetails.objects.get(user=request.user), saved=False, approved_by_warden=False).count()>0):
        return JsonResponse({"message": "Error", "status":"404"})
    else:
        print(params)
        outPass1=outPass.objects.get(outpassId=params['id'])
        outPass1.saved=False
        outPass1.save()
        generateNotification(outPass1,request, "SO")

        return JsonResponse({"message":"Sent", "status":"200"})

@api_view(['GET'])
@permission_classes((IsAuthenticated, StudentAccessPermissions,))
def generateOutpass(request, format=None):
    params=request.GET
    data=getOutpassDetails(params.get('id'))
    if(data!=None):
        return JsonResponse({"message":"Success", "data":json.dumps(data), "status":"200"})
    else:
        return JsonResponse({"message":"Error", "status":"404"})


# Get Full Details For Outpass
def getOutpassDetails(id):
    outpass=outPass.objects.get(outpassId=id)
    print(outPass)
    if(outpass.approved_by_warden==True):
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
        return data
    else:
        return None


@api_view(['PUT'])
@permission_classes((IsAuthenticated, StudentAccessPermissions, ))
def generateHash(request, format=None):
    #print(request.data)
    params=request.data
    code=params['code']

    f = Fernet(key)
    encrypted = f.encrypt(code.encode())
    print(encrypted)
    try:
        outpass=outPass.objects.get(outpassId=params['outpassId'], approved_by_warden=True)
        outpass.uniqueHash=code
        outpass.save()
        return JsonResponse({"message":"Success", "hashedCode":encrypted.decode() ,"status":"200"})
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Not Found","status":"404"})


@api_view(['GET'])
# @permission_classes((IsAuthenticated, StudentAccessPermissions, ))
def verifyHash(request, format=None):
    try:
        f = Fernet(key)
        code=request.GET.get("hashedCode")
        print(code.encode())
        decrypted = f.decrypt(code.encode())
        print(decrypted)
        print(str(decrypted)[2:len(decrypted)-1])

        outpass=outPass.objects.get(uniqueHash=str(decrypted)[2:len(str(decrypted))-1])
        data=getOutpassDetails(outpass.outpassId)

        if(data!=None):
            print(serializers.data[0])
            return JsonResponse({"message":"Success", "data":json.dumps(data), "status":"200"})
        else:
            return JsonResponse({"message":"Error", "status":"404"})
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Error", "status":"404"})


@api_view(['GET'])
# @permission_classes((IsAuthenticated, StudentAccessPermissions, ))
def todaysList(request, format=None):
    outpassList=outPass.objects.filter(fromDate=parse_date(request.GET.get('currentDate')))
    serializer=outPassSerializer(outpassList, many=True)
    return JsonResponse({"message":"Success", "outpassList":json.dumps(serializer.data), "status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, StudentAccessPermissions,))
def acceptedOutpassNotifications(request, format=None):
    accepted_outpassRequests=Notifications.objects.filter(receiver=UserDetails.objects.get(user=request.user), isRead=False)
    print(accepted_outpassRequests)
    for i in accepted_outpassRequests:
        i.isRead=True
        i.save()
    outpasses=NotificationsSerializer(accepted_outpassRequests, many=True)
    return JsonResponse({"message": "Success","accepted_outpasses":json.dumps(outpasses.data), "status":"200"})

@api_view(['GET'])
@permission_classes((IsAuthenticated, StudentAccessPermissions,))
def acceptedOutpassNotifications1(request, format=None):
    accepted_outpassRequests=Notifications.objects.filter(receiver=UserDetails.objects.get(user=request.user), isRead=False)
    print(accepted_outpassRequests)
    outpasses=NotificationsSerializer(accepted_outpassRequests, many=True)
    return JsonResponse({"message": "Success","accepted_outpasses":json.dumps(outpasses.data), "status":"200"})
