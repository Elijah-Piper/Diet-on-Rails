from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests

from .forms import CreateUserForm, AddSavedFoodForm

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
	'303': {'name': 'Iron', 'unit': 'mg'},
	'291': {'name': 'Fiber', 'unit': 'g'},
	'306': {'name': 'Potassium', 'unit': 'mg'},
	'307': {'name': 'Sodium', 'unit': 'mg'},
	'203': {'name': 'Protein', 'unit': 'g'},
	'269': {'name': 'Total Sugars', 'unit': 'g'},
	'539': {'name': 'Added Sugars', 'unit': 'g'},
	'324': {'name': 'Vitamin D', 'unit': 'IU'},
	'221': {'name': 'Alcohol, ethyl', 'unit': 'g'},
	'262': {'name': 'Caffeine', 'unit': 'mg'},
	'322': {'name': 'Carotene, alpha', 'unit': 'Âµg'},
	'321': {'name': 'Carotene, beta', 'unit': 'Âµg'},
	'421': {'name': 'Choline', 'unit': 'mg'},
	'417': {'name': 'Folate', 'unit': 'Âµg'},
	'431': {'name': 'Folic Acid', 'unit': 'Âµg'},
	'304': {'name': 'Magnesium', 'unit': 'mg'},
	'315': {'name': 'Manganese', 'unit': 'mg'},
	'305': {'name': 'Phosphorus', 'unit': 'mg'},
	'317': {'name': 'Selenium', 'unit': 'Âµg'},
	'309': {'name': 'Folate', 'unit': 'Âµg'},
	'417': {'name': 'Zinc', 'unit': 'mg'},
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

@login_required
def saved_foods(request):
	"""
	Displays any food items the user has chosen to save.
	"""
	context = dict()
	context['saved_foods'] = request.user.saved_foods.all()
	context['food_groups'] = request.user.grouped_foods.all()

	return render(request, 'saved_foods.html', context=context)

@login_required
def add_saved_food(request):
	"""
	Uses a search form to allow the user to choose a result to add to their
		SavedFoods model.
	"""
	context = {}

	if request.method == 'POST':
		form = AddSavedFoodForm(request.POST)
		if form.is_valid():
			# Brand name vs. USDA common foods in search results
			search_type = {'common': True, 'branded': True}
			if form.cleaned_data['food_type'] == '1':
				search_type['common'] = False
			elif form.cleaned_data['food_type'] == '2':
				search_type['branded'] = False
			results = food_lookup(
				query=form.cleaned_data['query'], 
				common=search_type['common'], 
				branded=search_type['branded']
			)
			context['results'] = results
	else:
		form = AddSavedFoodForm()

	context['form'] = form

	return render(request, 'add_saved_food.html', context=context)

### API endpoint interface (v2/search/instant) 
def food_lookup(query, common, branded) -> list:
		"""
		Takes a search query, queries the food API, and returns the search 
			results to be displayed by HTML.
		"""
		params = {
			'query': query,
			'common': common,
			'branded': branded,
			'self': False,
			'detailed': True,
		}
		headers = {
			'Content-Type': 'application/json',
			'x-app-id': '8447a624',
			'x-app-key': '3cab324652168f1b42f3df5abab15baf',
			'x-remote-user-id': '0',
		}

		response = requests.get(
			'https://trackapi.nutritionix.com/v2/search/instant',
			params=params,
			headers=headers,
		)

		json = response.json()
		food_list = []
		for category in json:
			# Combining categorical lists into a single list (if more than one)
			partial_food_list = json[category]
			food_list += partial_food_list
		results = {}
		for item in food_list:
			# The search results description to be displayed for the client
			description = {
				'serving': {'qty': item['serving_qty'], 'unit': item['serving_unit']},
				'weight': item['serving_weight_grams'],
				'image': item['photo']['thumb'],
			}
			try:
				description['brand'] = item['brand_name']
			except KeyError:
				description['brand'] = None
			for nutrient in item['full_nutrients']:
				attr_id = str(nutrient['attr_id'])
				nutrient_qty = nutrient['value']
				try:
					nutrient_name = NUTRITIONIX_USDA_NUTRIENT_MAPPING[attr_id]['name']
					nutrient_units = NUTRITIONIX_USDA_NUTRIENT_MAPPING[attr_id]['unit']

					description[nutrient_name] = {
						'qty': nutrient_qty, 
						'units': nutrient_units
					}
				except KeyError:
					pass
			results[item['food_name']] = description

		return results


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