from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect
from .form import SignUpForm
from django.contrib import messages
from .models import Profile
from .form1 import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponseRedirect

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
			profile = Profile(user = user,first_name = user.profile.first_name, last_name = user.profile.last_name)
			profile.save()

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
			profile = Profile.objects.get(pk=user.id)
			return render(request,'signup/profile.html',{'user': user,'profile':profile })
		else:
			messages.error(request,"Invalid username  or password.")
	else:
		messages.error(request, "Invalid username or password.")

	form =  AuthenticationForm()

	return render(request,'signup/login.html',{'form':form})

@login_required
def profile_view(request):

	args = {}
	if request.method == 'POST':
	
		#print(request.user)
		form = ProfileForm(request.POST,instance = request.user)
		form.actual_user = request.user
		if form.is_valid():
			user = form.save()
			
			user.refresh_from_db()

			user.profile.bio = form.cleaned_data.get('bio')
			user.profile.location = form.cleaned_data.get('location')
			user.profile.birthdate = form.cleaned_data.get('birthdate')
			
			user.save()
			return HttpResponseRedirect(reverse('login'))

	else:

		form = ProfileForm()


	args['form'] = form

	return render(request,'signup/edit.html',args)



@login_required
def logout_view(request):
	return render(request,'signup/logout.html')
