from django.contrib.auth.forms import UserCreationForm 
from django import forms
from . models import User,ServiceRequest,Feedback
class DateInput(forms.DateInput):
	input_type = 'date'

class TForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ["uname","username","gender","tflatno","phone_no","email"]
		
		

class SForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ["uname","username","gender","role_type","phone_no","email","provider_photo"]


class ReqForm(forms.ModelForm):
	class Meta:
		model= ServiceRequest
		fields=['role_type','tmobile','date']
		widgets = {
            'date': DateInput(),
        }
class FedForm(forms.ModelForm):
	class Meta:
		model=Feedback
		fields=['satisfaction','description','provider_uid']


''''
class AssignServiceProviderForm(forms.ModelForm):
	class Meta:
		model = ServiceRequest
		fields = ['role_type']  
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)# Filter available service providers based on the selected service type
		service_type = self.instance.role_type
		self.fields[''].queryset = User.objects.filter(role_type=service_type,  is_active=True)'''


		

