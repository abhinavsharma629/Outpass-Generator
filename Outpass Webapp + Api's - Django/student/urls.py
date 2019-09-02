from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

urlpatterns = [

    #IP:- 127.0.0.1:8000/student/

    #Api Views
    path('saveStudentDetails/', views.saveStudentDetails, name="saveStudentDetails"),
    path('registeredColleges', views.registeredColleges, name="registeredColleges"),
    path('pendingRequests', views.pendingRequests, name="pendingRequests"),
    path('studentDetails', views.studentDetails, name="studentDetails"),
    path('savedOutpass', views.savedOutpass, name="savedOutpass"),
    path('outpassHistory', views.outpassHistory, name="outpassHistory"),
    path('isVerified', views.isVerified, name="isVerified"),
    path('collegeWardens', views.collegeWardens, name="collegeWardens"),
    path('saveOutpass/', views.saveOutpass, name="saveOutpass"),
    path('sendOutpass/', views.sendOutpass, name="sendOutpass"),
    path('removePendingOutpass', views.removePendingOutpass, name="removePendingOutpass"),
    path('outpassDetails', views.outpassDetails, name="outpassDetails"),
    path('editOutpass/', views.editOutpass, name="editOutpass"),
    path('sendSavedOutpass/', views.sendSavedOutpass, name="sendSavedOutpass"),
    path('generateOutpass', views.generateOutpass, name="generateOutpass"),
    path('generateHash/', views.generateHash, name="generateHash"),
    path('verifyHash', views.verifyHash, name="verifyHash"),
    path('todaysList', views.todaysList, name="todaysList"),
    path("acceptedOutpassNotifications", views.acceptedOutpassNotifications, name="acceptedOutpassNotifications"),
    path("acceptedOutpassNotifications1", views.acceptedOutpassNotifications1, name="acceptedOutpassNotifications1"),

    #Render Views
    path('mainPage', views.mainPage, name="mainPage"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)
