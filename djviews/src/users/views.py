from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
from django.views.generic import CreateView
from .forms import RegisterForm



class RegisterView(CreateView):
	template_name= 'users/register.html'
	form_class = RegisterForm
	success_url = 'home'




class UserLoginView(LoginView):
	template_name='users/login.html'

class UserLogoutView(LogoutView):
	template_name='users/login.html'	
