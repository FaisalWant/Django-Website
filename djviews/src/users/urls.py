from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth import views as authViews

app_name= "users"

urlpatterns = [

    path('register/', RegisterView.as_view(), name="register" ),
    path('login/', UserLoginView.as_view(), name="login" ),
	path('logout/', UserLogoutView.as_view(), name="logout" ),
	path('password-change/', authViews.PasswordChangeView.as_view(), name="password_change" ),
    path('password-change-done/', authViews.PasswordChangeDoneView.as_view(), name="password_change_done" ),
      

   ]