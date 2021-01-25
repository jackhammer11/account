from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
   first_name = forms.CharField(max_length = 100,help_text = 'First Name')
   last_name = forms.CharField(max_length = 100,help_text = 'Last Name')
   email = forms.EmailField(max_length = 150,help_text='Email')
   birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')



   class Meta:
   		model = User
   		fields = ('username','first_name','last_name','email','birth_date','password1','password2',)