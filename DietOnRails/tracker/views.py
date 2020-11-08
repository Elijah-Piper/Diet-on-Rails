from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import ast
import requests
import urllib

from .forms import CreateUserForm, AddSavedFoodForm
from .models import SavedFood

# {attr_id: {name: ***, unit: ***}}
# If 'model_name' is False, the nutrient model field name is the same as 'name'
#	else: the model field name is provided in 'model_name'
NUTRITIONIX_USDA_NUTRIENT_MAPPING = {
	'301': {'name': 'calcium', 'unit': 'mg', 'model_name': False},
	'205': {'name': 'carbohydrate', 'unit': 'g', 'model_name': 'total_carbs'},
	'601': {'name': 'cholesterol', 'unit': 'mg', 'model_name': False},
	'208': {'name': 'energy', 'unit': 'kcal', 'model_name': 'calories'},
	'606': {'name': 'saturated', 'unit': 'g', 'model_name': 'saturated_fat'},
	'645': {'name': 'monounsaturated', 'unit': 'g', 'model_name': 'monounsaturated_fat'},
	'646': {'name': 'polyunsaturated', 'unit': 'g', 'model_name': 'polyunsaturated_fat'},
	'204': {'name': 'fat', 'unit': 'g', 'model_name': 'total_fat'},
	'605': {'name': 'trans', 'unit': 'g', 'model_name': 'trans_fat'},
	'303': {'name': 'iron', 'unit': 'mg', 'model_name': False},
	'291': {'name': 'fiber', 'unit': 'g', 'model_name': False},
	'306': {'name': 'potassium', 'unit': 'mg', 'model_name': False},
	'307': {'name': 'sodium', 'unit': 'mg', 'model_name': False},
	'203': {'name': 'protein', 'unit': 'g', 'model_name': 'total_protein'},
	'269': {'name': 'sugar', 'unit': 'g', 'model_name': 'total_sugar'},
	'539': {'name': 'added sugar', 'unit': 'g', 'model_name': 'added_sugar'},
	'324': {'name': 'vitamin d', 'unit': 'IU', 'model_name': 'vitamin_d'},
	'221': {'name': 'alcohol', 'unit': 'g', 'model_name': False},
	'262': {'name': 'caffeine', 'unit': 'mg', 'model_name': False},
	'322': {'name': 'carotene a', 'unit': 'Âµg', 'model_name': 'carotene_a'},
	'321': {'name': 'carotene b', 'unit': 'Âµg', 'model_name': 'carotene_b'},
	'421': {'name': 'choline', 'unit': 'mg', 'model_name': False},
	'417': {'name': 'folate', 'unit': 'Âµg', 'model_name': False},
	'431': {'name': 'folic acid', 'unit': 'Âµg', 'model_name': 'folic_acid'},
	'304': {'name': 'magnesium', 'unit': 'mg', 'model_name': False},
	'315': {'name': 'manganese', 'unit': 'mg', 'model_name': False},
	'305': {'name': 'phosphorus', 'unit': 'mg', 'model_name': False},
	'317': {'name': 'selenium', 'unit': 'Âµg', 'model_name': False},
	'309': {'name': 'zinc', 'unit': 'mg', 'model_name': False},
	'513': {'name': 'alanine', 'unit': 'g', 'model_name': False},
	'511': {'name': 'arginine', 'unit': 'mg', 'model_name': False},
	'514': {'name': 'aspartic acid', 'unit': 'g', 'model_name': 'aspartic_acid'},
	'454': {'name': 'betaine', 'unit': 'mg', 'model_name': False},
	'326': {'name': 'vitamin d3', 'unit': 'Âµg', 'model_name': 'vitamin_d3'},
	'207': {'name': 'ash', 'unit': 'g', 'model_name': False},
	'312': {'name': 'copper', 'unit': 'mg', 'model_name': False},
	'325': {'name': 'vitamin d2', 'unit': 'Âµg', 'model_name': 'vitamin_d2'},
	'507': {'name': 'cystine', 'unit': 'g', 'model_name': False},
	'851': {'name': 'omega-3 (ALA)', 'unit': 'g', 'model_name': 'omega_3_ala'},
	'629': {'name': 'omega-3 (EPA)', 'unit': 'g', 'model_name': 'omega_3_epa'},
	'631': {'name': 'omega-3 (DPA)', 'unit': 'g', 'model_name': 'omega_3_dpa'},
	'621': {'name': 'omega-3 (DHA)', 'unit': 'g', 'model_name': 'omega_3_dha'},
	'852': {'name': 'omega-3 (ETE)', 'unit': 'g', 'model_name': 'omega_3_ete'},
	'675': {'name': 'omega-6 (LA)', 'unit': 'g', 'model_name': 'omega_6_la'},
	'685': {'name': 'omega-6 (GLA)', 'unit': 'g', 'model_name': 'omega_6_gla'},
	'672': {'name': 'omega-6 (EA)', 'unit': 'g', 'model_name': 'omega_6_ea'},
	'853': {'name': 'omega-6 (DGLA)', 'unit': 'g', 'model_name': 'omega_6_dgla'},
	'855': {'name': 'omega-6 (AA)', 'unit': 'g', 'model_name': 'omega_6_aa'},
	'313': {'name': 'fluoride', 'unit': 'Âµg', 'model_name': False},
	'212': {'name': 'fructose', 'unit': 'g', 'model_name': False},
	'287': {'name': 'galactose', 'unit': 'g', 'model_name': False},
	'515': {'name': 'glutamic acid', 'unit': 'g', 'model_name': 'glutamic_acid'},
	'211': {'name': 'dextrose', 'unit': 'g', 'model_name': False},
	'516': {'name': 'glycine', 'unit': 'g', 'model_name': False},
	'512': {'name': 'histidine', 'unit': 'g', 'model_name': False},
	'521': {'name': 'hydroxyproline', 'unit': 'g', 'model_name': False},
	'503': {'name': 'isoleucine', 'unit': 'g', 'model_name': False},
	'213': {'name': 'lactose', 'unit': 'g', 'model_name': False},
	'504': {'name': 'leucine', 'unit': 'g', 'model_name': False},
	'337': {'name': 'lycopine', 'unit': 'Âµg', 'model_name': False},
	'505': {'name': 'lysine', 'unit': 'g', 'model_name': False},
	'214': {'name': 'maltose', 'unit': 'g', 'model_name': False},
	'506': {'name': 'methionine', 'unit': 'g', 'model_name': False},
	'406': {'name': 'niacin', 'unit': 'mg', 'model_name': False},
	'428': {'name': 'menaquinone-4', 'unit': 'g', 'model_name': 'menaquinone_4'},
	'410': {'name': 'pantothenic acid', 'unit': 'mg', 'model_name': False},
	'508': {'name': 'phenylalanine', 'unit': 'g', 'model_name': False},
	'636': {'name': 'phytosterols', 'unit': 'mg', 'model_name': False},
	'517': {'name': 'proline', 'unit': 'g', 'model_name': False},
	'319': {'name': 'retinol', 'unit': 'Âµg', 'model_name': False},
	'405': {'name': 'riboflavin', 'unit': 'mg', 'model_name': False},
	'518': {'name': 'serine', 'unit': 'mg', 'model_name': False},
	'209': {'name': 'starch', 'unit': 'g', 'model_name': False},
	'210': {'name': 'sucrose', 'unit': 'g', 'model_name': False},
	'406': {'name': 'theobromine', 'unit': 'mg', 'model_name': False},
	'404': {'name': 'thiamin', 'unit': 'mg', 'model_name': False},
	'502': {'name': 'threonine', 'unit': 'g', 'model_name': False},
	'323': {'name': 'vitamin e', 'unit': 'mg', 'model_name': 'vitamin_e'},
	'501': {'name': 'tryptophan', 'unit': 'g', 'model_name': False},
	'418': {'name': 'vitamin b12', 'unit': 'Âµg', 'model_name': 'vitamin_b12'},
	'415': {'name': 'vitamin b6', 'unit': 'mg', 'model_name': 'vitamin_b6'},
	'401': {'name': 'vitamin c', 'unit': 'mg', 'model_name': 'vitamin_c'},
	'430': {'name': 'vitamin k', 'unit': 'Âµg', 'model_name': 'vitamin_k'},
	'255': {'name': 'water', 'unit': 'g', 'model_name': False},
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
def add_food(request, food_query_string):
	"""
	Takes an encoded food information query string and creates a SavedFood 
		instance associated with the currently logged in user.
	"""
	# Decodes food nutrition information into dict from url parameter
	food = urllib.parse.parse_qs(food_query_string)
	for field in food:
		# Converts from list(string) to dictionary
		food[field] = ast.literal_eval(''.join(food[field]))
	
	# Instantiation of new SavedFood instance
	new_food = SavedFood(
		user=request.user,
		name=food['name']['string'],
		brand=food['brand'],
		serving_qty=food['serving']['qty'],
		serving_unit=food['serving']['unit'],
		serving_weight_g=food['weight']['qty'],
		image_url=food['image']['url'],
	)

	# Population of nutrient info available for the new SavedFood instance
	ignore_fields = ('name', 'serving', 'weight', 'image', 'brand')
	for field in food:
		if field not in ignore_fields:
			# Finds the model field name that this nutrient corresponds to
			attr_id = ''.join(tuple(
				att_id 
				for att_id in NUTRITIONIX_USDA_NUTRIENT_MAPPING
				if field == NUTRITIONIX_USDA_NUTRIENT_MAPPING[att_id]['name']
			))
			field_name = NUTRITIONIX_USDA_NUTRIENT_MAPPING[attr_id]['model_name']
			if not field_name:
				field_name = NUTRITIONIX_USDA_NUTRIENT_MAPPING[attr_id]['name']
			setattr(new_food, field_name, food[field]['qty'])

	new_food.save()

	return redirect('saved-foods')

@login_required
def food_search(request):
	"""
	Uses a search form to allow the user to choose a result to add to their
		SavedFood model.
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
				"protein", "carbohydrate", "fiber", "sugar", "added sugar", "fat", 
				"saturated", "monounsaturated", "polyunsaturated", "image", 
				"serving", "weight", "brand", "energy", 'sodium', 'encoded', 'name'
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
				'name': {'string': item['food_name']},
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
			# Encoded data for passing to a URL about the food item
			encoded = urllib.parse.urlencode(description)
			description['encoded'] = {'query_string': encoded}

			results[item['food_name']] = description

		return results