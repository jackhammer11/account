from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect
from .form import SignUpForm
from django.contrib import messages
from .models import Profile


def home_view(request):
	return render(request,'signup/home.html')


def signup_view(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.first_name = form.cleaned_data.get('first_name')
			user.profile.last_name= form.cleaned_data.get('last_name')
			user.profile.email= form.cleaned_data.get('email')
			user.profile.birth_date = form.cleaned_data.get('birth_date')
			user.save()

			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request,user)

			return redirect('home')

	else:
		form = SignUpForm()

	return render(request,'signup/signup.html',{'form':form})

def login_view(request):
	form = AuthenticationForm(request,request.POST)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')

		user = authenticate(username = username,password=password)

		if user is not None:
			login(request,user)
			messages.info(request,f"You are now logged in as {username}")
			profile = Profile.objects
			return render(request,'signup/profile.html',{'user': user,'profile':profile })
		else:
			messages.error(request,"Invalid username  or password.")
	else:
		messages.error(request, "Invalid username or password.")

	form =  AuthenticationForm()

	return render(request,'signup/login.html',{'form':form})
	
'''
def profile_view(request):

	return render(request,'signup/profile.html')
'''	