from django.forms import ModelForm
from .models import Profile 


class ProfileForm(ModelForm):
	class meta:
		model =Profile
		fields = ['user','first_name','last_name','bio','location','birthdate']

