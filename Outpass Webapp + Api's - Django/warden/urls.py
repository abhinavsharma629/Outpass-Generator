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

    #IP:- 127.0.0.1:8000/warden/

    #Api Views
    path('saveWardenDetails/', views.saveWardenDetails, name="saveWardenDetails"),
    path('wardenDetails', views.wardenDetails, name="wardenDetails"),
    path('pendingOutpassRequests', views.pendingOutpassRequests, name="pendingOutpassRequests"),
    path('acceptOutpass/', views.acceptOutpass, name="acceptOutpass"),
    path('acceptedOutpassRequests', views.acceptedOutpassRequests, name="acceptedOutpassRequests"),
    path('outpassOverview', views.outpassOverview, name="outpassOverview"),
    path('makeWardenRequests', views.makeWardenRequests, name="makeWardenRequests"),
    path('acceptWardenRequest', views.acceptWardenRequest, name="acceptWardenRequest"),
    path('deleteFakeWarden', views.deleteFakeWarden, name="deleteFakeWarden"),
    path('generateOutpass', views.generateOutpass, name="generateOutpass"),
    path('allpendingNotifications', views.allpendingNotifications, name="allpendingNotifications"),

    #Render Views
    path('mainPage', views.mainPage, name="mainPage"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)
