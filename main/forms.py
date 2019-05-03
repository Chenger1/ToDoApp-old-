from django import forms
from .models import Action, Category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class ActionForm(forms.ModelForm):
	categorys = forms.ModelMultipleChoiceField(queryset=None)
	
	def __init__(self, user,*args, **kwargs):
		super(ActionForm, self).__init__(*args, **kwargs)
		self.fields['categorys'].queryset=Category.objects.filter(user_id=user.id)


	class Meta:
		model = Action
		fields = [
			'name',
			'time_to_do_hour',
			'time_to_do_minute',
			'time_should_be_hour',
			'time_should_be_minute',
			'description',
			'categorys',
			'time_trigger'
		]
		labels ={
			'time_trigger':'Scheduled this action'
		}
		widgets = {
			'name':forms.TextInput(attrs={'id':'name_input'}),
			'slug':forms.TextInput(attrs={}),
			'time_trigger':forms.CheckboxInput(attrs={'type':'checkbox'}),
			'time_to_do_hour':forms.NumberInput(attrs={'class':'time_check currently'}),
			'time_to_do_minute':forms.NumberInput(attrs={'class':'time_check currently'}),
			'time_should_be_hour':forms.NumberInput(attrs={'class':'time_check'}),
			'time_should_be_minute':forms.NumberInput(attrs={'class':'time_check'}),
			'description':forms.Textarea(attrs={'style':'height:150px;'}),
		}
	def clean(self):
		time_to_do_hour = self.cleaned_data['time_to_do_hour']
		time_to_do_minute = self.cleaned_data['time_to_do_minute']
		time_should_be_hour = self.cleaned_data['time_should_be_hour']
		time_should_be_minute = self.cleaned_data['time_should_be_minute']
		time_trigger = self.cleaned_data['time_trigger']
		if time_to_do_hour == None and time_to_do_minute ==None and time_should_be_hour==None and time_should_be_minute==None:
			raise ValidationError({'time_should_be_minute':'','time_to_do_minute':'You must fill out at least one field.'}, code='empty exist')
		
		if time_to_do_hour == 0 and time_to_do_minute ==0 and time_should_be_hour==0 and time_should_be_minute==0:
			raise ValidationError({'time_to_do_minute':'All fields shouldn`t be zero.'}, code='zero exist')
		
		if time_trigger !=True:
			if time_to_do_hour == None and time_to_do_minute ==None:
				raise ValidationError({'time_to_do_minute':'If you want to schedule an action, please click on checkbox. If not, you must fill this fields'}, code='empty exist')
class CategoryForm(forms.ModelForm):

	def __init__(self, user, *args, **kwargs):
		super(CategoryForm, self).__init__(*args, **kwargs)
		self.user_id = user.id
	class Meta:
		model = Category
		fields=[
			'name',
		]
		widgets={
			'name':forms.TextInput(attrs={'class':'form-control'}),
		}

	def clean(self):
		name = self.cleaned_data['name']
		user_category = Category.objects.filter(user_id=self.user_id)
		if user_category:
			for item in user_category:
				if name == item.name:
					raise ValidationError({'name':'This category already register.'},code='name exists')

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
			'password_check',
		]

		widgets = {
			'username': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
		}

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		email = self.cleaned_data['email']
		if User.objects.filter(username=username).exists():
			raise ValidationError({'username':'This user already register.'},code='user exists')

		if password != password_check:
			raise ValidationError({'password':'','password_check':'Password does not exists.'}, code='Passwords do not exist.')


		if User.objects.filter(email=email).exists():
			raise ValidationError({'email':'This email already register.'}, code='This email already register.')

class LoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields=[
			'username',
			'password'
		]
		widgets={
			'username':forms.TextInput(attrs={'class':'form-control'})
		}
	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise ValidationError({'username':'This username does not register'}, code='user exits')

		user = User.objects.get(username=username)
		if user and not user.check_password(password):
			raise ValidationError({'password':'Password in wrong'}, code='password incorrect')