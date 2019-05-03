from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Action, Category
from .forms import ActionForm, CategoryForm, RegistrationForm, LoginForm
# Create your views here.
def action_view(request):
	try:
		model = Action.objects.filter(user=request.user).order_by('-id')
		action_model = []
		for item in model:
			if item.is_available:
				action_model.append(item) 
		category_model = Category.objects.filter(user=request.user)
		category_form = CategoryForm(request.user) 
		action_form = ActionForm(request.user)
		context={	'actions':action_model,
					'categorys':category_model,
					'category_form':category_form,
					'action_form':action_form}

		return render(request, 'main/actions.html',context )
	except:
		return render(request, 'main/first_look.html', context={'trigger':True})
def logout_view(request):
	logout(request)
	return redirect(reverse('action_url'))

def restore_view(request, slug):
	model = Action
	obj = model.objects.get(slug__iexact=slug)
	obj.is_available = True
	obj.save()
	return redirect(reverse('action_url'))

def hidden_view(request, slug):
	model = Action
	obj = model.objects.get(slug__iexact=slug)
	obj.is_available = False
	obj.save()
	return redirect(reverse('action_url'))

def delete_view(request, slug):
	if 'category-' in slug:
		model = Category
	else:
		model = Action
	obj = model.objects.get(slug__iexact=slug)
	obj.delete()
	return redirect(reverse('action_url'))

def category_view(request,slug):
	model = Category.objects.filter(slug__iexact=slug)
	return render(request, 'main/category_view.html', context={'model':model})

def history_view(request):
	action_model = Action.objects.filter(user=request.user).order_by('-id')
	return render(request, 'main/history.html', context={'actions':action_model})

def time_proccessing(times, time_trigger):
	for index, item in enumerate(times):
		if item == None:
			times[index]=0
	if time_trigger:
		if times[1]>=60:
			while times[1]>=60:
				times[0] +=1
				times[1]-=60
			return times
	else:
		if times[3]>=60:
			while times[3]>=60:
				times[2] +=1
				times[3]-=60
		if times[1] !=0:
			if times[1]>=60:
				while times[1]>=60:
					times[0] +=1
					times[1]-=60
			return times

class ActionsAddView(View):
	def post(self, request):
		form = ActionForm(request.user,request.POST, request.FILES)
		if form.is_valid():
			time_trigger = form.cleaned_data['time_trigger']
			name = form.cleaned_data['name']
			times = [
				form.cleaned_data['time_should_be_hour'],
				form.cleaned_data['time_should_be_minute'],
				form.cleaned_data['time_to_do_hour'],
				form.cleaned_data['time_to_do_minute'],
			]
			time_proccessing(times, time_trigger)
			description = form.cleaned_data['description']
			categorys = form.cleaned_data['categorys']
			new_action = Action.objects.create(
				user = request.user,
				name = name,
				time_to_do_hour = times[2],
				time_to_do_minute = times[3],
				time_should_be_hour = times[0],
				time_should_be_minute = times[1],
				time_trigger = time_trigger,
				description = description,
				)
			new_action.category.set(categorys)
			return redirect(reverse('action_url')) 
		return render(request, 'main/add_action.html', context={'forms':form})

class UpdateView(View):
	def post(self, request, slug):
		obj = Action.objects.get(slug__iexact=slug)
		form = ActionForm(request.user, request.POST,request.FILES,instance=obj)
		if form.is_valid():
			time_trigger = form.cleaned_data['time_trigger']
			times = [
				form.cleaned_data['time_should_be_hour'],
				form.cleaned_data['time_should_be_minute'],
				form.cleaned_data['time_to_do_hour'],
				form.cleaned_data['time_to_do_minute'],
			]
			time_proccessing(times, time_trigger)
			new_obj = form.save()
			new_obj.time_to_do_hour = times[2]
			new_obj.time_to_do_minute = times[3]
			new_obj.time_should_be_hour = times[0]
			new_obj.time_should_be_minute = times[1]
			new_obj.save()
			return redirect(reverse('action_url'))
		print(form.errors)
		return redirect(reverse('action_url'))

class CategoryAddView(View):
	def post(self, request):
		form = CategoryForm(request.user,request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			new_category = Category.objects.create(
				user = request.user,
				name = name
				)
			return redirect(reverse('action_url'))
		return render(request, 'main/add_category.html', context={'forms':form})

	def statictic(self, request, slug):
		model = Category.objects.get(slug__iexact=slug)
		return model

class RegisterView(View):
	def get(self, request):
		form = RegistrationForm()
		return render(request, 'main/register.html', context={'forms':form})

	def post(self, request):
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			login_user = authenticate(username=username, password=password)
			if login_user:
				login(request, login_user)
			return redirect(reverse('action_url'))
		return render(request,'main/register.html', context={'forms':form})	

class LoginView(View):
	def get(self, request):
		form = LoginForm
		return render(request, 'main/login.html', context={'forms':form})

	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			login_user = authenticate(username=username, password=password)
			if login_user:
				login(request, login_user)
				return redirect(reverse('action_url'))
		print(form.errors)
		return render(request, 'main/login.html', context={'forms':form})
