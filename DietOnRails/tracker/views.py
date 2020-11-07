from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests

from .forms import CreateUserForm, AddSavedFoodForm

# {attr_id: {name: ***, unit: ***}}
NUTRITIONIX_USDA_NUTRIENT_MAPPING = {
	'301': {'name': 'calcium', 'unit': 'mg'},
	'205': {'name': 'carbohydrate', 'unit': 'g'},
	'601': {'name': 'cholesterol', 'unit': 'mg'},
	'208': {'name': 'energy', 'unit': 'kcal'},
	'606': {'name': 'saturated', 'unit': 'g'},
	'645': {'name': 'monounsaturated', 'unit': 'g'},
	'646': {'name': 'polyunsaturated', 'unit': 'g'},
	'204': {'name': 'fat', 'unit': 'g'},
	'605': {'name': 'trans', 'unit': 'g'},
	'303': {'name': 'iron', 'unit': 'mg'},
	'291': {'name': 'fiber', 'unit': 'g'},
	'306': {'name': 'potassium', 'unit': 'mg'},
	'307': {'name': 'sodium', 'unit': 'mg'},
	'203': {'name': 'protein', 'unit': 'g'},
	'269': {'name': 'sugar', 'unit': 'g'},
	'539': {'name': 'a_sugar', 'unit': 'g'},
	'324': {'name': 'vitamin d', 'unit': 'IU'},
	'221': {'name': 'alcohol', 'unit': 'g'},
	'262': {'name': 'caffeine', 'unit': 'mg'},
	'322': {'name': 'crotene a', 'unit': 'Âµg'},
	'321': {'name': 'carotene b', 'unit': 'Âµg'},
	'421': {'name': 'choline', 'unit': 'mg'},
	'417': {'name': 'folate', 'unit': 'Âµg'},
	'431': {'name': 'folic acid', 'unit': 'Âµg'},
	'304': {'name': 'magnesium', 'unit': 'mg'},
	'315': {'name': 'manganese', 'unit': 'mg'},
	'305': {'name': 'phosphorus', 'unit': 'mg'},
	'317': {'name': 'selenium', 'unit': 'Âµg'},
	'309': {'name': 'folate', 'unit': 'Âµg'},
	'417': {'name': 'zinc', 'unit': 'mg'},
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
			context['display_exclusion'] = [
				"protein", "carbohydrate", "fiber", "sugar", "a_sugar", "fat", 
				"saturated", "monounsaturated", "polyunsaturated", "image", 
				"serving", "weight", "brand", "energy", 'sodium'
			]
			# For search result shortcuts in sidebar
			shortcut_ids = {}
			for food in results:
				brand = results[food]['brand']
				if brand:
					pass
				else:
					brand = 'USDA C.F.'
				display_text = f'{food} | {brand}'
				shortcut_ids[food] = display_text
				
			context['shortcut_ids'] = shortcut_ids
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
				'weight': {'qty': item['serving_weight_grams'], 'units': 'g'},
				'image': {'url': item['photo']['thumb']},
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
					if nutrient_units[0] == 'Â':
						nutrient_units = nutrient_units[1:]

					description[nutrient_name] = {
						'qty': nutrient_qty, 
						'units': nutrient_units
					}
				except KeyError:
					pass
			results[item['food_name']] = description

		return results