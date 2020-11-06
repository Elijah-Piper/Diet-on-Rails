from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests

from .forms import CreateUserForm

# {attr_id: {name: ***, unit: ***}}
NUTRITIONIX_USDA_NUTRIENT_MAPPING = {
	'301': {'name': 'Calcium, Ca', 'unit': 'mg'},
	'205': {'name': 'Carbohydrate,', 'unit': 'g'},
	'601': {'name': 'Cholesterol', 'unit': 'mg'},
	'208': {'name': 'Energy', 'unit': 'kcal'},
	'606': {'name': 'Saturated Fat', 'unit': 'g'},
	'645': {'name': 'Monounsaturated Fat', 'unit': 'g'},
	'646': {'name': 'Polyunsaturated Fat', 'unit': 'g'},
	'204': {'name': 'Total Fat', 'unit': 'g'},
	'605': {'name': 'Trans Fat', 'unit': 'g'},
	'303': {'name': 'Iron, Fe', 'unit': 'mg'},
	'291': {'name': 'Fiber', 'unit': 'g'},
	'306': {'name': 'Potassium, K', 'unit': 'mg'},
	'307': {'name': 'Sodium, Na', 'unit': 'mg'},
	'203': {'name': 'Protein', 'unit': 'g'},
	'269': {'name': 'Sugars, total', 'unit': 'g'},
	'539': {'name': 'Sugars, added', 'unit': 'g'},
	'324': {'name': 'Vitamin D', 'unit': 'IU'},
	'221': {'name': 'Alcohol, ethyl', 'unit': 'g'},
	'262': {'name': 'Caffeine', 'unit': 'mg'},
	'322': {'name': 'Carotene, alpha', 'unit': 'Âµg'},
	'321': {'name': 'Carotene, beta', 'unit': 'Âµg'},
	'421': {'name': 'Choline', 'unit': 'mg'},
	'417': {'name': 'Folate', 'unit': 'Âµg'},
	'431': {'name': 'Folic Acid', 'unit': 'Âµg'},
	'304': {'name': 'Magnesium, Mg', 'unit': 'mg'},
	'315': {'name': 'Manganese, Mn', 'unit': 'mg'},
	'305': {'name': 'Phosphorus, P', 'unit': 'mg'},
	'317': {'name': 'Selenium, Se', 'unit': 'Âµg'},
	'309': {'name': 'Folate', 'unit': 'Âµg'},
	'417': {'name': 'Zinc, Zn', 'unit': 'mg'},
}

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



### For testing API endpoints

def item_lookup_nutrients(request):
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

	#return render(request, 'item_lookup.html', {'food_data': food_data})

def item_search(request, query):

	request_data = {
		'query': query,
		'self': False,
		'detailed': True
	}
	request_headers = {
		'Content-Type': 'application/json',
		'x-app-id': '8447a624',
		'x-app-key': '3cab324652168f1b42f3df5abab15baf',
		'x-remote-user-id': '0',
	}
	response = requests.get(
		'https://trackapi.nutritionix.com/v2/search/instant',
		params=request_data,
		headers=request_headers,
	)

	json = response.json()
	food_data = list()
	if 'branded' in json:
		food_data += json['branded']
	if 'self' in json:
		food_data += json['common']

	print(food_data[0])