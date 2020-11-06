from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests

from .forms import CreateUserForm

def home(request):
	"""Home dashboard view of the Tracker web application."""
	return render(request, template_name="home.html", context=None)

def create_user(request):
	"""Creates a new user account using the built in UserCreationForm."""
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			raw_password = form.cleaned_data['password1']
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = CreateUserForm()

	return render(request, 'create_user.html', {'form': form})

def saved_foods(request):
	"""
	Displays any food items the user has chosen to save.
	"""
	context = dict()
	context['saved_foods'] = request.user.saved_foods.all()
	context['food_groups'] = request.user.grouped_foods.all()

	return render(request, 'saved_foods.html', context=context)

"""
def item_lookup(request):
	request_data = {
		"query": "%4 Great Value Cottage Cheese",
		"timezone": "US/Mountain"
	}
	request_headers = {
		'Content-Type': 'application/json',
		'x-app-id': '8447a624',
		'x-app-key': '3cab324652168f1b42f3df5abab15baf',
		'x-remote-user-id': '0',
	}
	response = requests.post(
		'https://trackapi.nutritionix.com/v2/natural/nutrients',
		json=request_data,
		headers=request_headers
	)
	json = response.json()
	food_data = json['foods'][0]

	print(type(food_data))
	for data in food_data:
		print(f'{data}: {food_data[data]}')

	return render(request, 'item_lookup.html', {'food_data': food_data})
	"""