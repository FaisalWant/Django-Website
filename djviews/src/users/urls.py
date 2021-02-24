from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name= "users"

urlpatterns = [

    path('register/', RegisterView.as_view(), name="register" ),
    path('login/', UserLoginView.as_view(), name="login" ),
	path('logout/', UserLogoutView.as_view(), name="logout" ),
      

   ]