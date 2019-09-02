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

    #IP:- 127.0.0.1:8000/user/

    #Api Views
    #path('getUserDetails/', views.getUserDetails, name="getUserDetails"),
    #path('deleteUserDetails/', views.deleteUserDetails, name="deleteUserDetails"),
    path('createUser/', views.createUser, name="createUser"),
    path('validateUser/', views.validateUser, name="validateUser"),

    # Your URLs...
    path('tokenDetails', views.tokenDetails, name="tokenDetails"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),



    #Render Views
    path("login", TemplateView.as_view(template_name="commonPanel/login.html")),
    path("signup", TemplateView.as_view(template_name="commonPanel/signup.html")),
    path("mainPage", views.mainPage, name="mainPage"),
    path("logout", LogoutView.as_view()),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)
