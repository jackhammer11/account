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
from django.template import RequestContext
from django.template.context_processors import csrf
from .decorators import unauthenticated_user
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
				
				profile = Profile(user = user,first_name = user.profile.first_name, last_name = user.profile.last_name)
				user.save()
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
		#user_id = 0
		context = {}
		context.update(csrf(request))


		form = AuthenticationForm(request,request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			user = authenticate(username = username,password=password)

			if user is not None:
				request.session['username'] = username
				login(request,user)
				user_id = user.id
				user_view(request,user.id)
				
				
				#messages.info(request,f"You are now logged in as {username}")

				
			else:
				messages.error(request,"Invalid username  or password.")

		form =  AuthenticationForm()

		return render(request,'signup/login.html',{'form':form})

def user_view(request,user_id):
	#print(args)
	#login(request,user_id)
	print("hello")
	profile = get_object_or_404(Profile,pk=user_id)
	#redirect('profile')
	return render(request,'signup/profile.html',{'profile':profile })

@login_required

def profile_view(request):
		args ={}

		if request.method == 'POST':
			
			
			form = ProfileForm(request.POST,instance = request.user)
			form.actual_user = request.user

			if form.is_valid():

				if request.session.has_key('username'):
					username = request.session['username']

				user = form.save()
			
				user.refresh_from_db()

				user.profile.bio = form.cleaned_data.get('bio',)
				user.profile.location = form.cleaned_data.get('location')
				user.profile.birthdate = form.cleaned_data.get('birthdate')
				user.profile.profile_pic = form.cleaned_data.get('profile_pic')
				user.save()
				return HttpResponseRedirect(reverse('login'))

		else:
			
			current_user = Profile.objects.get(user = request.user)
			#print(dir(current_user.values_list))
			#print(dir(current_user))
			#data = {"bio":"bio","location":"location","birthdate":"birthdate"}
		
			form = ProfileForm(instance = current_user)


		args['form'] = form

		return render(request,'signup/edit.html',args)



@login_required
def logout_view(request):
	try:
		del request.session['username']
	except:
		pass

	logout(request)
	return render(request,'signup/logout.html')
	
