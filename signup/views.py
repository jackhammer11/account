from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect





def home_view(request):
	return render(request,'home.html')


def signup_view(request):
	pass